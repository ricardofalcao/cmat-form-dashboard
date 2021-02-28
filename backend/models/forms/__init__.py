from fastapi_users import models
from fastapi_users.db.sqlalchemy import GUID
from sqlalchemy import Column
from tortoise import models as tmodels


class Form(models.BaseModel):
    pass


class AlchemyModel:
    id = Column(GUID, primary_key=True)
