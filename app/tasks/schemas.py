from pydantic import BaseModel, Field
from datetime import datetime

class CreateTaskSchema(BaseModel):
    title : str = Field(..., max_length=100, min_length=3)
    description : str | None = Field(max_length=300, default=None)
    is_done : bool = Field(default=False)
    
class ResponseTaskSchema(BaseModel):
    id : int
    title : str = Field(..., max_length=100, min_length=3)
    description : str | None = Field(max_length=300, default=None)
    is_done : bool = Field(default=False)
    created_date : datetime = Field(..., description="creation date and time of the task")
    updated_date : datetime = Field(..., description="updating date and time of the task")

class UpdateTaskSchema(BaseModel):
    title : str | None = Field(default=None, max_length=100)
    description : str | None = Field(default=None, max_length=300)
    is_done : bool | None = Field(default=None)