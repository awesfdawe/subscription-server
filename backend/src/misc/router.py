from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from src.config import get_settings
from src.database import get_session
from src.models import Admins

settings = get_settings()

router = APIRouter(prefix="/misc", tags=["misc"])


@router.get("/is_first_setup_done")
def is_first_setup_done(session: Session = Depends(get_session)):
    existing_admin = session.exec(select(Admins)).first()
    if existing_admin:
        return {"ready": True}
    else:
        return {"ready": False}
