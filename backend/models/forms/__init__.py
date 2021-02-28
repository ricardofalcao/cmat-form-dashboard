from fastapi_users import models
from fastapi_users.db.sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, Session


class Form(models.BaseModel):
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

    __mapper_args__ = {'polymorphic_on': userId}
