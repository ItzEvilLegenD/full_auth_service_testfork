from sqlalchemy import Column, Integer, String
from query_database import Base

class User(Base):
    __tablename__ = "users" # Имя таблицы в БД

    # колонки таблицы, соответствующие схеме UserCreate
    # user_id будет первичным ключом
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)
    age = Column(Integer, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True) # Email должен быть уникальным
    role = Column(String, nullable=True)
    username = Column(String, unique=True, index=True) # Username тоже уникальный
    password = Column(String) # Храним хешированный пароль
