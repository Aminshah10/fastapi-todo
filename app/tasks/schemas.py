from pydantic import BaseModel, Field

class CreateTaskSchema(BaseModel):
    title : str = Field(..., max_length=100, min_length=3)
    description : str | None = Field(max_length=300, default=None)
    is_done : bool = Field(default=False)
    
class ResponseTaskSchema(CreateTaskSchema):
    id : int
    
class UpdateTaskSchema(BaseModel):
    title : str | None = Field(default=None, max_length=100)
    description : str | None = Field(default=None, max_length=300)
    is_done : bool | None = Field(default=None)