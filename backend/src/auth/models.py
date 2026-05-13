from sqlmodel import Field, SQLModel


class Admin(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(min_length=3, max_length=40)
    hashed_password: str = Field(max_length=255)
    password_version: int = Field(default=1)
