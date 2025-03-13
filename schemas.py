from pydantic import BaseModel

class ToDoCreate(BaseModel):
    """
    Pydantic model for creating a To-Do item.
    """
    task: str

class ToDoResponse(ToDoCreate):
    """
    Pydantic model for returning To-Do data with an ID.
    """
    id: int

    class Config:
        orm_mode = True
