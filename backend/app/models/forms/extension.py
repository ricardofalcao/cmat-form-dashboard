import uuid
from datetime import date
from typing import Optional, List

from fastapi_users.db.sqlalchemy import GUID
from pydantic import UUID4, validator
from sqlalchemy import Column, String, Date, Text, DateTime, func, ForeignKey, Table
from sqlalchemy.orm import relationship, Session

from dbase import Base
from models.forms import Form, AlchemyModel
from models.user import User


#
#
#

class ExtensionFormBase(Form):
    id: Optional[UUID4] = None
    type: str
    description: str
    observations: Optional[str] = None

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()


class ExtensionForm(ExtensionFormBase):
    user: User
    members: List[User]
    dateStart: date
    dateFinish: date

    class Config:
        orm_mode = True


class ExtensionFormCreate(ExtensionFormBase):
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


user_association_table: Table = Table('form_extension_members', Base.metadata,
                               Column('member_id', GUID, ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
                               Column('form_id', GUID, ForeignKey('form_extension.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
                               )


class AlchemyExtensionFormModel(Base, AlchemyModel):
    __tablename__ = "form_extension"

    members = relationship("AlchemyUserModel", secondary=user_association_table)

    type = Column(String(length=64), index=True, nullable=False)
    description = Column(Text, nullable=False)

    dateStart = Column(Date, index=True, nullable=False)
    dateFinish = Column(Date, index=True, nullable=False)

    observations = Column(Text, nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def postUpdate(self, db: Session, create_model: ExtensionFormCreate):
        this_members_ids = map(lambda m: m.id, self.members)

        for member in create_model.members:
            if member not in this_members_ids:
                db.execute(user_association_table.insert(), params={'member_id': member, 'form_id': self.id})

        self.members = [x for x in self.members if x.id in create_model.members]

        db.commit()
        db.refresh(self)

    def postInsert(self, db: Session, create_model: ExtensionFormCreate):
        for member in create_model.members:
            db.execute(user_association_table.insert(), params={'member_id': member, 'form_id': self.id})

        db.commit()
        db.refresh(self)
