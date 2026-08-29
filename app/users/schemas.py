from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime


class LoginUserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=72)


class RegisterUserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=72)
    confirm_password: str = Field(min_length=8, max_length=72)

    @model_validator(mode="after")
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

        return self


class UserResponseSchema(BaseModel):
    id: int
    username: str
    is_active: bool
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)

class RefreshTokenSchema(BaseModel):
    refresh_token: str