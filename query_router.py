from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import query_crud as crud
import query_schemas as schemas
from query_database import get_db_session

router = APIRouter()

@router.post("/register", response_model=schemas.UserRead, status_code=201)
async def add_user_endpoint(user: schemas.UserCreate, db: AsyncSession = Depends(get_db_session)):
    """
    Эндпоинт для добавления нового пользователя в базу данных.
    Принимает данные пользователя в теле запроса.
    """
    # Проверка на существование пользователя с таким же email или username или id
    db_user_by_email = await crud.get_user_by_email(db, email=user.email)
    db_user_by_username = await crud.get_user_by_username(db, username=user.username)
    db_user_by_id = await crud.get_user(db, user_id=user.user_id)
    if db_user_by_email or db_user_by_username or db_user_by_id:

        return JSONResponse(status_code=409, detail="User already exists")
    # комментирую это потому что не уверен, что эта функция добавляет пользователя в бд. 
    # если добавляет, то все гуд. если не добавляет, то тут надо сделать так, 
    # чтобы пользователь добавлялся в бд
    await crud.create_user(db=db, user=user)
    return JSONResponse(status_code=201, detail="Registered successfully")

@router.post("/signin", response_model=schemas.UserRead, status_code=201)
async def add_user_endpoint(user: schemas.UserCreate, db: AsyncSession = Depends(get_db_session)):
    """
    Эндпоинт для добавления нового пользователя в базу данных.
    Принимает данные пользователя в теле запроса.
    """
    # Проверка на существование пользователя с таким же email или username
    db_user_by_email = await crud.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user_by_username = await crud.get_user_by_username(db, username=user.username)
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="Username already exists")
    # Проверка на существование user_id (если он должен быть уникальным и не автогенерируемым БД)
    db_user_by_id = await crud.get_user(db, user_id=user.user_id)
    if db_user_by_id:
         raise HTTPException(status_code=400, detail=f"User ID {user.user_id} already exists")

    created_user = await crud.create_user(db=db, user=user)
    return created_user


@router.post("/add_user", response_model=schemas.UserRead, status_code=201)
async def add_user_endpoint(user: schemas.UserCreate, db: AsyncSession = Depends(get_db_session)):
    """
    Эндпоинт для добавления нового пользователя в базу данных.
    Принимает данные пользователя в теле запроса.
    """
    # Проверка на существование пользователя с таким же email или username
    db_user_by_email = await crud.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user_by_username = await crud.get_user_by_username(db, username=user.username)
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="Username already exists")
    # Проверка на существование user_id (если он должен быть уникальным и не автогенерируемым БД)
    db_user_by_id = await crud.get_user(db, user_id=user.user_id)
    if db_user_by_id:
         raise HTTPException(status_code=400, detail=f"User ID {user.user_id} already exists")

    created_user = await crud.create_user(db=db, user=user)
    return created_user

@router.delete("/delete_user/{user_id}", response_model=schemas.UserRead)
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db_session)):
    """
    Эндпоинт для удаления пользователя по user_id.
    """
    deleted_user = await crud.delete_user(db=db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user # вернуть данные удаленного пользователя

@router.get("/get_user/{user_id}", response_model=schemas.UserRead)
async def get_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db_session)):
    """
    Эндпоинт для получения информации о пользователе по user_id.
    """
    db_user = await crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/get_all_users", response_model=List[schemas.UserRead])
async def get_all_users_endpoint(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)):
    """
    Эндпоинт для получения списка всех пользователей с пагинацией.
    """
    users = await crud.get_users(db=db, skip=skip, limit=limit)
    return users