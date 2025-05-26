from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

import query_models as models
import query_schemas as schemas

async def get_user(db: AsyncSession, user_id: int):
    """Получает пользователя по user_id."""
    result = await db.execute(select(models.User).filter(models.User.user_id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str):
    """Получает пользователя по email."""
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str):
    """Получает пользователя по username."""
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получает список пользователей."""
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    """Создает нового пользователя в БД."""
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    """Удаляет пользователя по user_id."""
    db_user = await get_user(db, user_id)
    if db_user:
        await db.execute(delete(models.User).where(models.User.user_id == user_id))
        #await db.delete(db_user) # Если объект уже загружен
        await db.commit()
        return db_user
    return None