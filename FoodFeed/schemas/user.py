# Create user
from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str


# Edit user