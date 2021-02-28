import uuid
from datetime import date
from typing import Optional, List

from fastapi_users.db.sqlalchemy import GUID
from pydantic import UUID4, validator
from sqlalchemy import Column, String, Date, Text, DateTime, func, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base
from models.forms import Form, AlchemyModel
from models.user import User


#
#
#

class EventOrganizationFormBase(Form):
    id: Optional[UUID4] = None
    eventType: str
    involvementType: str
    regionType: str
    designation: str
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
        return v

    def create_update_dict(self):
        this_dict = self.dict(
            exclude_unset=True,
            exclude={"date", "members"}
        )

        return {**this_dict, 'dateStart': self.date[0], 'dateFinish': self.date[1], 'id': self.id}


user_association_table = Table('form_event_organization_members', Base.metadata,
                               Column('member_id', GUID, ForeignKey('user.id')),
                               Column('form_id', GUID, ForeignKey('form_event_organization.id'))
                               )

class AlchemyEventOrganizationFormModel(Base, AlchemyModel):
    __tablename__ = "form_event_organization"

    userId = Column(GUID, ForeignKey("user.id"))
    user = relationship("AlchemyUserModel")

    members = relationship("AlchemyUserModel", secondary=user_association_table)

    eventType = Column(String(length=64), index=True, nullable=False)
    involvementType = Column(String(length=64), index=True, nullable=False)
    regionType = Column(String(length=64), index=True, nullable=False)
    designation = Column(String(length=64), index=True, nullable=False)
    local = Column(String(length=64), index=True, nullable=False)

    dateStart = Column(Date, index=True, nullable=False)
    dateFinish = Column(Date, index=True, nullable=False)

    url = Column(Text, nullable=False)
    observations = Column(Text, nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
