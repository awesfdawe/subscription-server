from fastapi import APIRouter, Depends
from sqlmodel import Session
from argon2 import PasswordHasher

from src.config import get_settings
from src.database import get_session
from src.auth.dependencies import get_current_admin

settings = get_settings()

ph = PasswordHasher()

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/protected_get")
def protected_get(admin: int = Depends(get_current_admin), session: Session = Depends(get_session)):
    return {"id": admin}


@router.post("/protected_post")
def protected_post(admin: int = Depends(get_current_admin), session: Session = Depends(get_session)):
    return {"id": admin}
