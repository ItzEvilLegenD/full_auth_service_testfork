from fastapi import APIRouter
from dependencies.auth_depends import authenticate_user, register_user
from pydantic import BaseModel
import webbrowser
from typing import Optional

router = APIRouter()

class LoginRequest(BaseModel):
    user_id: int
    username: str
    hashed_password: str
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = "user"

@router.post("/register")
def register(register_data: LoginRequest):
    header_data = register_user(register_data.username, register_data.password)
    webbrowser.open_new_tab('http://localhost:8000/docs#/')
    return header_data

@router.post("/signin")
def signin(login_data: LoginRequest):
    header_data = authenticate_user(login_data.username, login_data.password)
    webbrowser.open_new_tab('http://localhost:8000/docs#/')
    return header_data