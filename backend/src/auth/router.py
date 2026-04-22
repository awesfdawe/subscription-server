from fastapi import APIRouter, Depends, HTTPException, status, Response
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt

from src.config import get_settings
from src.database import get_session
from src.auth.schemas import RegisterRequest, TokenPayload
from src.models import Admins

settings = get_settings()

ph = PasswordHasher()

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(user: RegisterRequest, session: Session = Depends(get_session)):
    existing_admin = session.exec(select(Admins)).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An admin account has already been created. Only one account is allowed. Please try logging in.",
        )

    db_user = Admins.model_validate(user, update={"hashed_password": ph.hash(user.password)})
    session.add(db_user)
    session.commit()
    return {"detail": "Successfully registered."}


@router.post("/login")
def login(user: RegisterRequest, response: Response, session: Session = Depends(get_session)):
    db_user = session.exec(select(Admins)).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The admin account has not been created yet. Please try registering.",
        )
    try:
        if db_user.username == user.username and ph.verify(db_user.hashed_password, user.password):
            secure = True
            if settings.environment == "dev":
                secure = False

            access_payload = TokenPayload(user_id=db_user.id, exp=datetime.now(timezone.utc) + timedelta(hours=2))
            response.set_cookie(
                key="access_token",
                value=jwt.encode(
                    access_payload.model_dump(),
                    settings.jwt_secret,
                    algorithm="HS256",
                ),
                httponly=True,
                secure=secure,
                samesite="lax",
                max_age=7200,  # 2h
                expires=7200,
                path="/api",
            )
            return {"detail": "Successfully logged in."}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    except VerifyMismatchError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
