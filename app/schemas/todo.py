from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class TodoAddSchema(BaseModel):
    name: str = Field(max_length=100)
    description: Optional[str] = Field(max_length=1000)
    completed: bool = False


class TodoUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TodoSchema(TodoAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
