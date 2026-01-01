# Post CRUD
from pydantic import BaseModel

class ContentCreate(BaseModel):
    author: str
    body: str

class ContentView(BaseModel):
    id: int
    author: str
    body: str

    class Config:
        orm_mode = True