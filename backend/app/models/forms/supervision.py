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

class SupervisionFormBase(Form):
    id: Optional[UUID4] = None
    student: str
    studentCountry: str
    type: str
    situation: str
    title: str
    institution: str
    course: str
    observations: Optional[str] = None

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()


class SupervisionForm(SupervisionFormBase):
    user: User
    supervisors: List[User]
    dateStart: date
    dateFinish: date

    class Config:
        orm_mode = True


class SupervisionFormCreate(SupervisionFormBase):
    date: List[date]
    supervisors: List[UUID4]

    @validator("supervisors")
    def supervisors_empty(cls, v):
        assert len(v) > 0, 'The supervisors list cannot be empty!'
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
            exclude={"date", "id", "supervisors"}
        )

        return {**this_dict, 'dateStart': self.date[0], 'dateFinish': self.date[1]}


user_association_table: Table = Table('form_supervision_supervisors', Base.metadata,
                               Column('supervisor_id', GUID, ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
                               Column('form_id', GUID, ForeignKey('form_supervision.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
                               )


class AlchemySupervisionFormModel(Base, AlchemyModel):
    __tablename__ = "form_supervision"

    supervisors = relationship("AlchemyUserModel", secondary=user_association_table)

    student = Column(String(length=64), index=True, nullable=False)
    studentCountry = Column(String(length=64), index=True, nullable=False)
    type = Column(String(length=64), index=True, nullable=False)
    situation = Column(String(length=64), index=True, nullable=False)
    title = Column(String(length=128), index=True, nullable=False)
    institution = Column(String(length=64), index=True, nullable=False)
    course = Column(String(length=64), index=True, nullable=False)

    dateStart = Column(Date, index=True, nullable=False)
    dateFinish = Column(Date, index=True, nullable=False)

    observations = Column(Text, nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def postUpdate(self, db: Session, create_model: SupervisionFormCreate):
        this_supervisors_ids = map(lambda m: m.id, self.supervisors)

        for supervisor in create_model.supervisors:
            if supervisor not in this_supervisors_ids:
                db.execute(user_association_table.insert(), params={'supervisor_id': supervisor, 'form_id': self.id})

        self.supervisors = [x for x in self.supervisors if x.id in create_model.supervisors]

        db.commit()
        db.refresh(self)

    def postInsert(self, db: Session, create_model: SupervisionFormCreate):
        for supervisor in create_model.supervisors:
            db.execute(user_association_table.insert(), params={'supervisor_id': supervisor, 'form_id': self.id})

        db.commit()
        db.refresh(self)
