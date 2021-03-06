import uuid
from typing import Optional

from pydantic import UUID4, validator
from sqlalchemy import Column, String, Text, DateTime, func, Integer

from dbase import Base
from models.forms import Form, AlchemyModel
from models.user import User


#
#
#

class ReferringEditorialActFormBase(Form):
    id: Optional[UUID4] = None
    type: str
    regionType: str
    publicationType: str
    publication: str
    reviews: int
    year: int
    observations: Optional[str] = None

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()


class ReferringEditorialActForm(ReferringEditorialActFormBase):
    user: User

    class Config:
        orm_mode = True


class ReferringEditorialActFormCreate(ReferringEditorialActFormBase):
    def create_dict(self):
        return {**self.update_dict(), 'id': self.id}

    def update_dict(self):
        this_dict = self.dict(
            exclude_unset=True,
            exclude={"id"}
        )

        return {**this_dict}


class AlchemyReferringEditorialActFormModel(Base, AlchemyModel):
    __tablename__ = "form_referring_editorial_act"

    type = Column(String(length=64), index=True, nullable=False)
    regionType = Column(String(length=64), index=True, nullable=False)
    publicationType = Column(String(length=64), index=True, nullable=False)
    publication = Column(String(length=256), index=True, nullable=False)

    reviews = Column(Integer, index=True, nullable=False)
    year = Column(Integer, index=True, nullable=False)

    observations = Column(Text, nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
