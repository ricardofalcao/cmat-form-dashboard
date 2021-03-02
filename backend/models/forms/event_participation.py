import uuid
from datetime import date
from typing import Optional, List

from fastapi_users.db.sqlalchemy import GUID
from pydantic import UUID4, validator
from sqlalchemy import Column, String, Date, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from dbase import Base
from models.forms import Form, AlchemyModel
from models.user import User


#
#
#

class EventParticipationFormBase(Form):
    id: Optional[UUID4] = None
    eventType: str
    participationType: str
    title: Optional[str] = None
    event: str
    local: str
    observations: Optional[str] = None

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()


class EventParticipationForm(EventParticipationFormBase):
    user: User
    dateStart: date
    dateFinish: date

    class Config:
        orm_mode = True

class EventParticipationFormCreate(EventParticipationFormBase):
    date: List[date]

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
            exclude={"date", "id"}
        )

        return {**this_dict, 'dateStart': self.date[0], 'dateFinish': self.date[1]}


class AlchemyEventParticipationFormModel(Base, AlchemyModel):
    __tablename__ = "form_event_participation"

    eventType = Column(String(length=64), index=True, nullable=False)
    participationType = Column(String(length=64), index=True, nullable=False)
    title = Column(String(length=64), index=True, nullable=True)
    event = Column(String(length=64), index=True, nullable=False)
    local = Column(String(length=64), index=True, nullable=False)

    dateStart = Column(Date, index=True, nullable=False)
    dateFinish = Column(Date, index=True, nullable=False)

    observations = Column(Text, nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
