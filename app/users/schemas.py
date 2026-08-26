from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class LoginUserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=72)


class RegisterUserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=72)
    confirm_password: str = Field(min_length=8, max_length=72)
    
class UserResponseSchema(BaseModel):
    id: int
    username: str
    is_active: bool
    created_date: datetime
    
    model_config = ConfigDict(from_attributes=True)
    