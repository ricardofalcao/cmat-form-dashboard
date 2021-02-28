from typing import Optional, List

from fastapi_users import models
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String

from database import Base


class User(models.BaseUser):
    name: Optional[str] = None

    class Config:
        orm_mode = True

class UserList(models.BaseModel):
    users: List[User] = []

class UserCreate(models.BaseUserCreate):
    name: str


class UserUpdate(User, models.BaseUserUpdate):
    name: Optional[str]

class UserDB(User, models.BaseUserDB):
    pass

class AlchemyUserModel(Base, SQLAlchemyBaseUserTable):
    name = Column(String(length=64), index=True, nullable=False)