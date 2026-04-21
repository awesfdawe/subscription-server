from pydantic import BaseModel, Field
from datetime import datetime


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=200)


class TokenPayload(BaseModel):
    user_id: int
    exp: datetime
