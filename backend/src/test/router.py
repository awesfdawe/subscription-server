from fastapi import APIRouter, Depends

from src.config import get_settings
from src.auth.dependencies import get_current_admin

settings = get_settings()

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/protected_get")
def protected_get(admin: int = Depends(get_current_admin)):
    return {"id": admin}


@router.post("/protected_post")
def protected_post(admin: int = Depends(get_current_admin)):
    return {"id": admin}
