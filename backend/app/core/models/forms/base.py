from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, Session

from core.utils import GUID


class Form(BaseModel):
    def create_dict(self):
        pass

    def update_dict(self):
        pass


class AlchemyFormModel:
    id = Column(GUID, primary_key=True)

    @declared_attr
    def userId(cls):
        return Column(GUID, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))

    @declared_attr
    def user(cls):
        return relationship("AlchemyUserModel", foreign_keys=[cls.userId])

    def postInsert(self, db: Session, create_model):
        pass

    def postUpdate(self, db: Session, create_model):
        pass

    __mapper_args__ = {'polymorphic_on': userId}
