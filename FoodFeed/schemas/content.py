# Post CRUD
from pydantic import BaseModel

class ContentCreate(BaseModel):
    #author: str
    #image: None
    body: str

class ContentView(BaseModel):
    id: int
    author: str
    image: None
    body: str