import enum
from typing import Optional, List

from fastapi_users import models
from fastapi_users.db import SQLAlchemyBaseUserTable
from pydantic import EmailStr
from sqlalchemy import Column, String, Enum

from db import Base


class UserGroup(str, enum.Enum):
    ALC = "ALC"
    ANAP = "ANAP"
    GTA = "GTA"
    SAPOR = "SAPOR"

class UserType(str, enum.Enum):
    MA = "MA"
    MC = "MC"
    MI = "MI"
    STUDENT = "STUDENT"
    OTHER = "OTHER"

class UserPosition(str, enum.Enum):
    ASSISTANT_PROFESSOR = "ASSISTANT_PROFESSOR"
    ASSOCIATE_PROFESSOR = "ASSOCIATE_PROFESSOR"
    ADJUNCT_PROFESSOR = "ADJUNCT_PROFESSOR"
    FULL_PROFESSOR = "FULL_PROFESSOR"
    JUNIOR_RESEARCHER = "JUNIOR_RESEARCHER"
    POSTDOC_RESEARCHER = "POSTDOC_RESEARCHER"
    SCHOLARSHIP = "SCHOLARSHIP"

class User(models.BaseUser):
    gmail: Optional[EmailStr] = None
    name: Optional[str] = None
    shortName: Optional[str] = None
    authorName: Optional[str] = None
    group: Optional[UserGroup] = None
    institution: Optional[str] = None
    type: Optional[UserType] = None
    position: Optional[UserPosition] = None
    cienciaId: Optional[str] = None
    orcidId: Optional[str] = None
    scopusAuthorId: Optional[str] = None
    researcherId: Optional[str] = None

    class Config:
        orm_mode = True

class UserList(models.BaseModel):
    users: List[User] = []

class UserCreate(models.BaseUserCreate):
    gmail: EmailStr
    name: str
    shortName: str
    authorName: str
    group: UserGroup
    institution: str
    type: UserType
    position: UserPosition
    cienciaId: Optional[str] = None
    orcidId: Optional[str] = None
    scopusAuthorId: Optional[str] = None
    researcherId: Optional[str] = None

class UserUpdate(User, models.BaseUserUpdate):
    pass

class UserDB(User, models.BaseUserDB):
    pass

class AlchemyUserModel(Base, SQLAlchemyBaseUserTable):
    gmail = Column(String(length=320), unique=True, index=True, nullable=False)
    name = Column(String(length=256), index=True, nullable=False)
    shortName = Column(String(length=64), index=True, nullable=False)
    authorName = Column(String(length=64), index=True, nullable=False)
    group = Column(Enum(UserGroup), index=True, nullable=False)
    institution = Column(String(length=64), index=True, nullable=False)
    type = Column(Enum(UserType), index=True, nullable=False)
    position = Column(Enum(UserPosition), index=True, nullable=False)
    cienciaId = Column(String(length=64), index=True, nullable=True)
    orcidId = Column(String(length=64), index=True, nullable=True)
    scopusAuthorId = Column(String(length=64), index=True, nullable=True)
    researcherId = Column(String(length=64), index=True, nullable=True)