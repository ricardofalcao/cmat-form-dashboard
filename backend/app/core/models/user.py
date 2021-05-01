import enum
import uuid
from typing import Optional, List

from pydantic import EmailStr, UUID4, BaseModel, validator
from sqlalchemy import Column, String, Enum, Boolean

from db import Base
from core.utils import GUID


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

class User(BaseModel):
    id: UUID4
    email: EmailStr
    gmail: EmailStr
    name: str
    shortName: str
    authorName: str
    is_superuser: bool
    group: UserGroup
    institution: str
    type: UserType
    position: UserPosition
    cienciaId: Optional[str]
    orcidId: Optional[str]
    scopusAuthorId: Optional[str]
    researcherId: Optional[str]

    class Config:
        orm_mode = True

class UserList(BaseModel):
    users: List[User] = []

class UserCreate(User):
    id: Optional[UUID4] = None
    is_superuser: Optional[bool] = False
    password: str

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()

    def create_dict(self):
        return self.dict(exclude_unset=True)

class UserUpdate(BaseModel):
    id: Optional[UUID4] = None
    email: Optional[EmailStr] = None
    gmail: Optional[EmailStr] = None
    name: Optional[str] = None
    shortName: Optional[str] = None
    authorName: Optional[str] = None
    is_superuser: Optional[bool] = False
    password: Optional[str]
    group: Optional[UserGroup] = None
    institution: Optional[str] = None
    type: Optional[UserType] = None
    position: Optional[UserPosition] = None
    cienciaId: Optional[str] = None
    orcidId: Optional[str] = None
    scopusAuthorId: Optional[str] = None
    researcherId: Optional[str] = None

    def update_dict(self):
        return self.dict(exclude_unset=True, exclude={"id", "is_superuser"})

class UserDB(User):
    hashed_password: str

    class Config:
        orm_mode = True

class AlchemyUserModel(Base):
    __tablename__ = "user"

    id = Column(GUID, primary_key=True)
    email = Column(String(length=320), unique=True, index=True, nullable=False)
    gmail = Column(String(length=320), unique=True, index=True, nullable=False)
    name = Column(String(length=256), index=True, nullable=False)
    shortName = Column(String(length=64), index=True, nullable=False)
    authorName = Column(String(length=64), index=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    hashed_password = Column(String(length=72), nullable=False)
    group = Column(Enum(UserGroup), index=True, nullable=False)
    institution = Column(String(length=64), index=True, nullable=False)
    type = Column(Enum(UserType), index=True, nullable=False)
    position = Column(Enum(UserPosition), index=True, nullable=False)
    cienciaId = Column(String(length=64), index=True, nullable=True)
    orcidId = Column(String(length=64), index=True, nullable=True)
    scopusAuthorId = Column(String(length=64), index=True, nullable=True)
    researcherId = Column(String(length=64), index=True, nullable=True)