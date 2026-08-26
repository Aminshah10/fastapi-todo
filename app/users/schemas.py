from pydantic import BaseModel

class LoginUserSchema(BaseModel):
    username: str
    password: str
    
class RegisterUserSchema(BaseModel):
    username: str
    password: str
    confirm_password: str
    