from fastapi import HTTPException, status, Cookie
from pydantic import ValidationError
import jwt

from src.config import get_settings
from .schemas import TokenPayload
from .utils import get_admin

settings = get_settings()


def is_admin(access_token: str | None = Cookie(default=None)):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in. Please log in.")
    print(f"Token from cookie: {access_token}")
    admin = get_admin()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The admin account has not been created yet. Please try registering.",
        )

    try:
        raw_payload = jwt.decode(access_token, settings.jwt_secret, algorithms=["HS256"])

        payload = TokenPayload(**raw_payload)

        if payload.password_version == admin.password_version:
            return
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in. Please log in.")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token structure is invalid.")
