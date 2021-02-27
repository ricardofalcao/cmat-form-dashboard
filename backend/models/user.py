from typing import Optional, List

from fastapi_users import models
from fastapi_users.db import TortoiseBaseUserModel
from tortoise import fields


class User(models.BaseUser):
    name: Optional[str] = None

class UserList(models.BaseModel):
    users: List[User] = []

class UserCreate(models.BaseUserCreate):
    name: str


class UserUpdate(User, models.BaseUserUpdate):
    name: Optional[str]

class UserDB(User, models.BaseUserDB):
    pass

class TortoiseUserModel(TortoiseBaseUserModel):
    name = fields.CharField(index=True, null=False, max_length=64)