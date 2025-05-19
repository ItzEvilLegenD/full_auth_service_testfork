from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    user_id: int
    username: str
    password: str
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = "user"

class UserRead(BaseModel):
    user_id: int
    username: str
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = "user"

    class Config:
        from_attributes = True