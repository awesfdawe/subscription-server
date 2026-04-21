from fastapi import HTTPException, status, Cookie
from pydantic import ValidationError
import jwt

from src.config import get_settings
from src.auth.schemas import TokenPayload

settings = get_settings()


def get_current_admin(access_token: str | None = Cookie(default=None)):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in. Please log in.")

    try:
        payload = jwt.decode(access_token, settings.jwt_secret, algorithms=["HS256"])

        payload = TokenPayload(**payload)

        return payload.user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token structure is invalid.")
