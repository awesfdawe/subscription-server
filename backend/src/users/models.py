from sqlmodel import Field, SQLModel
from datetime import datetime


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(min_length=3, max_length=40)
    description: str = Field(default="", max_length=400)
    expire_time: datetime
    enabled: bool = Field(default=True)
