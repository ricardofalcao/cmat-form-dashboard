import uuid
from datetime import date
from typing import Optional, List

from fastapi_users import models
from pydantic import UUID4, validator
from tortoise import fields, models as tmodels

from models.user import User


class Form(models.BaseModel):
    pass

class TortoiseFormModel(tmodels.Model):
    async def to_dict(self):
        d = {}
        for field in self._meta.db_fields:
            d[field] = getattr(self, field)
        for field in self._meta.backward_fk_fields:
            d[field] = await getattr(self, field).all().values()
        return d

    class Meta:
        abstract = True

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
    date_start: date
    date_finish: date

class EventParticipationFormList(models.BaseModel):
    forms: List[EventParticipationForm]

class EventParticipationFormCreate(EventParticipationFormBase):
    date: List[date]

    @validator("date")
    def date_order(cls, v):
        assert len(v) == 2, 'The number of date elements must be 2!'
        return v

class TortoiseEventParticipationFormModel(TortoiseFormModel):
    id = fields.UUIDField(pk=True, generated=False)
    user = fields.ForeignKeyField('models.TortoiseUserModel', related_name='user')
    eventType = fields.CharField(index=True, null=False, max_length=64)
    participationType = fields.CharField(index=True, null=False, max_length=64)
    title = fields.CharField(index=True, null=True, max_length=64)
    event = fields.CharField(index=True, null=False, max_length=64)
    local = fields.CharField(index=True, null=False, max_length=64)
    date_start = fields.DateField(index=True, null=False)
    date_finish = fields.DateField(index=True, null=False)
    observations = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)