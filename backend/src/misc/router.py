from fastapi import APIRouter

from src.config import get_settings
from src.auth.utils import get_admin

settings = get_settings()

router = APIRouter(prefix="/misc", tags=["misc"])


@router.get("/is_first_setup_done")
def is_first_setup_done():
    if get_admin():
        return {"ready": True}
    else:
        return {"ready": False}
