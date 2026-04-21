from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from argon2 import PasswordHasher

from src.config import get_settings
from src.database import get_session
from src.auth.models import RegisterRequest
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
            detail="An admin account has already been created. Only one account is allowed.",
        )

    db_user = Admins.model_validate(user, update={"hashed_password": ph.hash(user.password)})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/login")
def login(user: RegisterRequest, session: Session = Depends(get_session)):
    db_user = session.exec(select(Admins)).first()
    if db_user.username == user.username and ph.verify(db_user.hashed_password, user.password):
        return db_user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
