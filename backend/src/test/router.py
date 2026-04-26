from fastapi import APIRouter, Depends

from src.config import get_settings
from src.auth.dependencies import is_admin

settings = get_settings()

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/protected_get", dependencies=[Depends(is_admin)])
def protected_get():
    return "authorized"


@router.post("/protected_post", dependencies=[Depends(is_admin)])
def protected_post():
    return "authorized"
