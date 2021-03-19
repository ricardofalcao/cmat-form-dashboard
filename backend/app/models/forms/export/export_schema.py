import uuid
from typing import Optional, List

from fastapi_users.db.sqlalchemy import GUID
from pydantic import UUID4, validator, BaseModel
from sqlalchemy import Column, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from db import Base
from models import User


#
#
#

class ExportSchemaBase(BaseModel):
    id: Optional[UUID4] = None
    name: str
    template: str
    extension: str

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()

class ExportSchema(ExportSchemaBase):
    user: User
    type: str

    class Config:
        orm_mode = True

class ExportSchemaList(BaseModel):
    schemas: List[ExportSchema]


class ExportSchemaCreate(ExportSchemaBase):
    def create_dict(self):
        return {**self.update_dict(), 'id': self.id}

    def update_dict(self):
        this_dict = self.dict(
            exclude_unset=True,
            exclude={}
        )

        return {**this_dict}


class AlchemyExportSchemaModel(Base):
    __tablename__ = "export_schemas"

    id = Column(GUID, primary_key=True)

    userId = Column(GUID, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    user = relationship("AlchemyUserModel")

    type = Column(String(length=64), index=True, nullable=False)
    name = Column(String(length=64), index=True, nullable=False)
    template = Column(Text, nullable=False)
    extension = Column(String(length=64), index=True, nullable=False, default="txt")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
