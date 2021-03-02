from fastapi_users.db.sqlalchemy import GUID
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, Session


class Form(BaseModel):
    def create_dict(self):
        pass

    def update_dict(self):
        pass


class AlchemyModel:
    id = Column(GUID, primary_key=True)

    @declared_attr
    def userId(cls):
        return Column(GUID, ForeignKey("user.id"))

    @declared_attr
    def user(cls):
        return relationship("AlchemyUserModel")

    def postInsert(self, db: Session, create_model):
        pass

    def postUpdate(self, db: Session, create_model):
        pass

    __mapper_args__ = {'polymorphic_on': userId}
