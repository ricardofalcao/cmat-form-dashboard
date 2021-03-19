import uuid
from datetime import date
from typing import Optional, List

from fastapi_users.db.sqlalchemy import GUID
from pydantic import UUID4, validator
from sqlalchemy import Column, String, Date, Text, DateTime, func, ForeignKey, Table
from sqlalchemy.orm import relationship, Session

from db import Base
from models.forms import Form, AlchemyModel
from models.user import User


#
#
#

class JuryScientificCommitteeFormBase(Form):
    id: Optional[UUID4] = None
    type: str
    description: str
    observations: Optional[str] = None

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()


class JuryScientificCommitteeForm(JuryScientificCommitteeFormBase):
    user: User
    member: User
    dateStart: date
    dateFinish: date

    class Config:
        orm_mode = True


class JuryScientificCommitteeFormCreate(JuryScientificCommitteeFormBase):
    date: List[date]
    member: UUID4

    @validator("date")
    def date_order(cls, v):
        assert len(v) == 2, 'The number of date elements must be 2!'
        v.sort()

        return v

    def create_dict(self):
        return {**self.update_dict(), 'id': self.id}

    def update_dict(self):
        this_dict = self.dict(
            exclude_unset=True,
            exclude={"date", "id", "member"}
        )

        return {**this_dict, 'dateStart': self.date[0], 'dateFinish': self.date[1], 'memberId': self.member}


class AlchemyJuryScientificCommitteeFormModel(Base, AlchemyModel):
    __tablename__ = "form_jury_scientific_committee"

    memberId = Column(GUID, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    member = relationship("AlchemyUserModel", foreign_keys=[ memberId ])

    type = Column(String(length=64), index=True, nullable=False)
    description = Column(String(length=64), index=True, nullable=False)

    dateStart = Column(Date, index=True, nullable=False)
    dateFinish = Column(Date, index=True, nullable=False)

    observations = Column(Text, nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
