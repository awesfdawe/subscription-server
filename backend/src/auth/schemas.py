from pydantic import BaseModel, Field, model_validator
from datetime import datetime


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=40)
    password: str = Field(min_length=8, max_length=200)


class TokenPayload(BaseModel):
    password_version: int
    exp: datetime


class UpdateRequest(BaseModel):
    old_password: str = Field(min_length=8, max_length=200)
    new_username: str | None = Field(default=None, min_length=3, max_length=40)
    new_password: str | None = Field(default=None, min_length=8, max_length=200)

    @model_validator(mode="after")
    def at_least_one_field_exist(self) -> UpdateRequest:
        if self.new_username is None and self.new_password is None:
            raise ValueError("Atleast one field should exist: new_username, new_password")
        return self
