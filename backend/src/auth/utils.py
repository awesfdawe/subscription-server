from sqlmodel import select
from functools import lru_cache

from src.database import db_session
from .models import Admin


@lru_cache(maxsize=1)
def get_admin() -> Admin:
    with db_session() as session:
        admin = session.exec(select(Admin)).first()
        return admin
