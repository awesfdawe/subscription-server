from sqlalchemy import String
from sqlmodel import Field, SQLModel

class Admins(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(min_length=3, max_length=30)
    hashed_password: str = Field(sa_type=String(255))