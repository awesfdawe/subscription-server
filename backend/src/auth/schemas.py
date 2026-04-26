from pydantic import BaseModel, Field
from datetime import datetime


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=40)
    password: str = Field(min_length=8, max_length=200)


class TokenPayload(BaseModel):
    password_version: int
    exp: datetime
