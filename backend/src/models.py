from sqlalchemy import String
from sqlmodel import Field, SQLModel
from datetime import datetime


SQLModel.metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Admins(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(min_length=3, max_length=30)
    hashed_password: str = Field(sa_type=String(255))


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(min_length=3, max_length=40)
    description: str = Field(min_length=1, max_length=400)
    expire_time: datetime
    enabled: bool = Field(default=True)
