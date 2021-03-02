from datetime import date
from typing import List, Optional

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_users import FastAPIUsers, models
from pydantic import UUID4
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from starlette import status

from dbase import get_database
from models import *


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
            'user',
            'group',
            'eventType',
            'participationType',
            'title',
            'event',
            'local',
            'dateStart'
        ],
        search_fields=[
            'user',
            'group',
            'eventType',
            'participationType',
            'title',
            'event',
            'local'
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
            'user',
            'eventType',
            'involvementType',
            'designation',
            'local',
            'dateStart'
        ],
        search_fields=[
            'user',
            'eventType',
            'involvementType',
            'designation',
            'local'
        ]
    )

    __register_form_routes(
        forms_router,
        fastapi_users,
        'extension',
        ExtensionForm,
        ExtensionFormCreate,
        AlchemyExtensionFormModel,
        allowed_sorts=[
            'user',
            'type',
            'dateStart'
        ],
        search_fields=[
            'user',
            'type',
        ]
    )

    __register_form_routes(
        forms_router,
        fastapi_users,
        'supervision',
        SupervisionForm,
        SupervisionFormCreate,
        AlchemySupervisionFormModel,
        allowed_sorts=[
            'user',
            'student',
            'studentCountry',
            'type',
            'situation',
            'title',
            'institution',
            'course',
            'dateStart'
        ],
        search_fields=[
            'user',
            'student',
            'studentCountry',
            'type',
            'situation',
            'title',
            'institution',
            'course',
            'type',
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
        allowed_sorts: List[str] = [],
        search_fields: List[str] = []
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
            **form.create_dict(),
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

    @router.patch(f"/{form_name}/{{id:uuid}}", response_model=form_model)
    async def formUpdate(
            id: UUID4,
            form: form_create_model,
            user: User = Depends(fastapi_users.current_user()),
            db: Session = Depends(get_database)
    ):
        db_form = db.query(form_db_model).filter(form_db_model.id == id).first()
        if db_form is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if (not user.is_superuser) and (db_form.userId != user.id):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Only admins can update non owned forms')

        for key, value in form.update_dict().items():
            setattr(db_form, key, value)

        db.commit()
        db.refresh(db_form)

        db_form.postUpdate(db, form)

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
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Only admins can delete non owned forms')

        db.query(form_db_model).filter(form_db_model.id == id).delete()
        db.commit()

        return None

    def formListBase(
            query: sqlalchemy.orm.Query,
            size: int,
            page: int,
            date_from: Optional[date] = None,
            date_to: Optional[date] = None,
            sort: Optional[str] = None,
            desc: Optional[str] = None,
            q: Optional[str] = None,
    ):
        query = query.join(AlchemyUserModel)

        if q:
            filters = []
            for field in search_fields:
                if field == 'user':
                    attr = AlchemyUserModel.name
                elif field == 'group':
                    attr = AlchemyUserModel.group
                else:
                    attr = getattr(form_db_model, field, None)

                if attr:
                    filters.append(attr.contains(q))

            if len(filters) > 0:
                query = query.filter(or_(*filters))

        attr = getattr(form_db_model, 'dateStart', None)
        if attr:
            if date_from and date_to and date_to < date_from:
                temp = date_to
                date_to = date_from
                date_from = temp

            if date_from:
                query = query.filter(attr >= date_from)

            if date_to:
                query = query.filter(attr <= date_to)

        if sort and sort in allowed_sorts:
            if sort == 'user':
                attr = AlchemyUserModel.name
            elif sort == 'group':
                attr = AlchemyUserModel.group
            else:
                attr = getattr(form_db_model, sort, None)

            if attr:
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

    @router.get(f"/{form_name}/list/me", response_model=FormList)
    async def formListMe(
            size: int,
            page: int,
            date_from: Optional[date] = None,
            date_to: Optional[date] = None,
            sort: Optional[str] = None,
            desc: Optional[str] = None,
            q: Optional[str] = Query(None, min_length=3),
            user: User = Depends(fastapi_users.current_user()),
            db: Session = Depends(get_database),
    ):
        query = db.query(form_db_model, func.count(form_db_model.id).over().label('total')).filter(
            form_db_model.userId == user.id)

        return formListBase(
            query,
            size,
            page,
            date_from,
            date_to,
            sort,
            desc,
            q
        )

    @router.get(f"/{form_name}/list", response_model=FormList)
    async def formList(
            size: int,
            page: int,
            date_from: Optional[date] = None,
            date_to: Optional[date] = None,
            sort: Optional[str] = None,
            desc: Optional[str] = None,
            q: Optional[str] = Query(None, min_length=3),
            user: User = Depends(fastapi_users.current_user(superuser=True)),
            db: Session = Depends(get_database),
    ):
        query = db.query(form_db_model, func.count(form_db_model.id).over().label('total'))

        return formListBase(
            query,
            size,
            page,
            date_from,
            date_to,
            sort,
            desc,
            q
        )

    @router.post(f"/{form_name}/exports", response_model=ExportSchema)
    async def exportsCreate(
            export: ExportSchemaCreate,
            user: User = Depends(fastapi_users.current_user(superuser=True)),
            db: Session = Depends(get_database)
    ):

        created_export = AlchemyExportSchemaModel(
            **export.create_dict(),
            userId=user.id,
            type=form_name
        )

        db.add(created_export)
        db.commit()
        db.refresh(created_export)

        return created_export

    @router.patch(f"/{form_name}/exports/{{id:uuid}}", response_model=ExportSchema)
    async def exportsUpdate(
            id: UUID4,
            export: ExportSchemaCreate,
            user: User = Depends(fastapi_users.current_user(superuser=True)),
            db: Session = Depends(get_database)
    ):

        schema = db.query(AlchemyExportSchemaModel).filter(AlchemyExportSchemaModel.id == id).first()
        if schema is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        for key, value in export.update_dict().items():
            setattr(schema, key, value)

        db.commit()
        db.refresh(schema)

        return schema

    @router.delete(f"/{form_name}/exports/{{id:uuid}}", status_code=status.HTTP_204_NO_CONTENT)
    async def exportsDelete(
            id: UUID4,
            user: User = Depends(fastapi_users.current_user(superuser=True)),
            db: Session = Depends(get_database)
    ):

        schema = db.query(AlchemyExportSchemaModel).filter(AlchemyExportSchemaModel.id == id).first()
        if schema is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        db.query(AlchemyExportSchemaModel).filter(AlchemyExportSchemaModel.id == id).delete()
        db.commit()

        return schema

    @router.get(f"/{form_name}/exports/list", response_model=ExportSchemaList)
    async def exportsList(
            user: User = Depends(fastapi_users.current_user(superuser=True)),
            db: Session = Depends(get_database)
    ):

        schemas = db.query(AlchemyExportSchemaModel).filter(AlchemyExportSchemaModel.type == form_name).all()
        return ExportSchemaList(schemas=schemas)
