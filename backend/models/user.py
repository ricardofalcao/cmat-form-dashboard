import enum
from typing import Optional, List

from fastapi_users import models
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, Enum

from dbase import Base


class UserGroup(str, enum.Enum):
    ALC = "ALC"
    ANAP = "ANAP"
    GTA = "GTA"
    SAPOR = "SAPOR"

class User(models.BaseUser):
    name: Optional[str] = None
    group: Optional[UserGroup] = None

    class Config:
        orm_mode = True

class UserList(models.BaseModel):
    users: List[User] = []

class UserCreate(models.BaseUserCreate):
    name: str
    group: UserGroup

class UserUpdate(User, models.BaseUserUpdate):
    name: Optional[str]
    group: Optional[UserGroup]

class UserDB(User, models.BaseUserDB):
    pass

class AlchemyUserModel(Base, SQLAlchemyBaseUserTable):
    name = Column(String(length=64), index=True, nullable=False)
    group = Column(Enum(UserGroup), index=True, nullable=False)