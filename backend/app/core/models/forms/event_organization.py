import uuid
from datetime import date
from typing import Optional, List

from pydantic import UUID4, validator
from sqlalchemy import Column, String, Date, Text, DateTime, func, ForeignKey, Table, Integer
from sqlalchemy.orm import relationship, Session

from db import Base
from core.models.forms.base import Form, AlchemyFormModel
from core.models import User
from core.utils import GUID


#
#
#

class EventOrganizationFormBase(Form):
    id: Optional[UUID4] = None
    eventType: str
    involvementType: str
    regionType: str
    designation: str
    participants: int
    local: str
    url: str
    observations: Optional[str] = None

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()


class EventOrganizationForm(EventOrganizationFormBase):
    user: User
    members: List[User]
    dateStart: date
    dateFinish: date

    class Config:
        orm_mode = True


class EventOrganizationFormCreate(EventOrganizationFormBase):
    date: List[date]
    members: List[UUID4]

    @validator("members")
    def members_empty(cls, v):
        assert len(v) > 0, 'The members list cannot be empty!'
        return v

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
            exclude={"date", "id", "members"}
        )

        return {**this_dict, 'dateStart': self.date[0], 'dateFinish': self.date[1]}


user_association_table: Table = Table('form_event_organization_members', Base.metadata,
                                      Column('member_id', GUID,
                                             ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"),
                                             primary_key=True),
                                      Column('form_id', GUID,
                                             ForeignKey('form_event_organization.id', ondelete="CASCADE",
                                                        onupdate="CASCADE"), primary_key=True)
                                      )


class AlchemyEventOrganizationFormModel(Base, AlchemyFormModel):
    __tablename__ = "form_event_organization"

    members = relationship("AlchemyUserModel", secondary=user_association_table)

    eventType = Column(String(length=64), index=True, nullable=False)
    involvementType = Column(String(length=64), index=True, nullable=False)
    regionType = Column(String(length=64), index=True, nullable=False)
    designation = Column(String(length=64), index=True, nullable=False)
    participants = Column(Integer, index=True, nullable=False)
    local = Column(String(length=64), index=True, nullable=False)

    dateStart = Column(Date, index=True, nullable=False)
    dateFinish = Column(Date, index=True, nullable=False)

    url = Column(Text, nullable=False)
    observations = Column(Text, nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def postUpdate(self, db: Session, create_model: EventOrganizationFormCreate):
        this_members_ids = map(lambda m: m.id, self.members)

        for member in create_model.members:
            if member not in this_members_ids:
                db.execute(user_association_table.insert(), params={'member_id': member, 'form_id': self.id})

        self.members = [x for x in self.members if x.id in create_model.members]

        db.commit()
        db.refresh(self)

    def postInsert(self, db: Session, create_model: EventOrganizationFormCreate):
        for member in create_model.members:
            db.execute(user_association_table.insert(), params={'member_id': member, 'form_id': self.id})

        db.commit()
        db.refresh(self)
