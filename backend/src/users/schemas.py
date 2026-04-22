from pydantic import BaseModel, Field
from datetime import datetime


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=40)
    description: str = Field(min_length=1, max_length=400)
    expire_time: datetime
    enabled: bool = Field(default=True)


class UserUpdateRequest(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=40)
    description: str | None = Field(default=None, min_length=1, max_length=400)
    expire_time: datetime | None = None
    enabled: bool | None = None
