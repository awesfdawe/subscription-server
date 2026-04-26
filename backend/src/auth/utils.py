from sqlmodel import select
from functools import lru_cache

from src.database import db_session
from .models import Admins


@lru_cache(maxsize=1)
def get_admin() -> Admins:
    with db_session() as session:
        admin = session.exec(select(Admins)).first()
        return admin
