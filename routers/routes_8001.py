from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from models.user import User
from dependencies.auth_depends import authenticate_user, register_user
import json
from pydantic import BaseModel
import webbrowser

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

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