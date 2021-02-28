from typing import List, Optional

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers, models
from pydantic import UUID4
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from starlette import status

from database import get_database
from models.forms import Form, AlchemyModel
from models.forms.event_organization import EventOrganizationFormCreate, \
    EventOrganizationForm, AlchemyEventOrganizationFormModel
from models.forms.event_participation import EventParticipationForm, EventParticipationFormCreate, \
    AlchemyEventParticipationFormModel
from models.user import User


def register_form_routes(router: APIRouter, fastapi_users: FastAPIUsers):
    forms_router = APIRouter()

    __register_form_routes(
        forms_router,
        fastapi_users,
        'event-participation',
        EventParticipationForm,
        EventParticipationFormCreate,
        AlchemyEventParticipationFormModel,
        allowed_sorts=[
            'eventType',
            'participationType',
            'title',
            'event',
            'local',
        ]
    )

    __register_form_routes(
        forms_router,
        fastapi_users,
        'event-organization',
        EventOrganizationForm,
        EventOrganizationFormCreate,
        AlchemyEventOrganizationFormModel,
        allowed_sorts=[
            'eventType',
            'involvementType',
            'designation',
            'local',
        ]
    )

    router.include_router(
        forms_router,
        prefix="/forms"
    )


def __register_form_routes(
        router: APIRouter,
        fastapi_users: FastAPIUsers,
        form_name: str,
        form_model: Form,
        form_create_model: Form,
        form_db_model: AlchemyModel,
        allowed_sorts: List[str] = []
):
    class FormList(models.BaseModel):
        forms: List[form_model]
        total: Optional[int]

    @router.post(f"/{form_name}", response_model=form_model, status_code=status.HTTP_201_CREATED)
    async def formCreate(
            form: form_create_model,
            user: User = Depends(fastapi_users.current_user()),
            db: Session = Depends(get_database)
    ):

        created_form = form_db_model(
            **form.create_update_dict(),
            userId=user.id,
        )

        db.add(created_form)
        db.commit()
        db.refresh(created_form)

        created_form.postInsert(db, form)

        return created_form

    @router.get(f"/{form_name}/{{id:uuid}}", response_model=form_model)
    async def formGet(
            id: UUID4,
            user: User = Depends(fastapi_users.current_user(superuser=True)),
            db: Session = Depends(get_database)
    ):
        db_form = db.query(form_db_model).filter(form_db_model.id == id).first()
        if db_form is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return db_form

    @router.delete(f"/{form_name}/{{id:uuid}}", status_code=status.HTTP_204_NO_CONTENT)
    async def formDelete(
            id: UUID4,
            user: User = Depends(fastapi_users.current_user()),
            db: Session = Depends(get_database)
    ):
        db_form = db.query(form_db_model).filter(form_db_model.id == id).first()
        if db_form is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if (not user.is_superuser) and (db_form.userId != user.id):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Only admins can delete non owned forms')

        db.query(form_db_model).filter(form_db_model.id == id).delete()
        db.commit()

        return None

    @router.get(f"/{form_name}/list/me", response_model=FormList)
    async def formListMe(
            size: int,
            page: int,
            sort: Optional[str] = None,
            desc: Optional[str] = None,
            user: User = Depends(fastapi_users.current_user()),
            db: Session = Depends(get_database),
    ):
        query = db.query(form_db_model, func.count(form_db_model.id).over().label('total')).filter(form_db_model.userId == user.id)

        if sort and sort in allowed_sorts:
            attr = getattr(form_db_model, sort, None)

            if attr:
                attr = getattr(form_db_model, sort, None)
                query = query.order_by(sqlalchemy.asc(attr) if desc == "false" else sqlalchemy.desc(attr))

        query = query.limit(size)
        query = query.offset((page - 1) * size)

        result = query.all()

        forms = []
        total = 0

        for u in result:
            total = u[1]
            forms.append(u[0])

        return FormList(forms=forms, total=total)

    @router.get(f"/{form_name}/list", response_model=FormList)
    async def formList(
            size: int,
            page: int,
            sort: Optional[str] = None,
            desc: Optional[str] = None,
            user: User = Depends(fastapi_users.current_user(superuser=True)),
            db: Session = Depends(get_database),
    ):
        query = db.query(form_db_model, func.count(form_db_model.id).over().label('total'))

        if sort and sort in allowed_sorts:
            attr = getattr(form_db_model, sort, None)

            if attr:
                attr = getattr(form_db_model, sort, None)
                query = query.order_by(sqlalchemy.asc(attr) if desc == "false" else sqlalchemy.desc(attr))

        query = query.limit(size)
        query = query.offset((page - 1) * size)

        result = query.all()

        forms = []
        total = 0

        for u in result:
            total = u[1]
            forms.append(u[0])

        return FormList(forms=forms, total=total)
