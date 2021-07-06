from typing import TypeVar, Generic

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic.generics import GenericModel
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status

from core import controllers
from db import get_database
from core.models import *

DataT = TypeVar('DataT')


class FormList(GenericModel, Generic[DataT]):
    forms: List[DataT]
    total: Optional[int]


def register_form_routes(router: APIRouter):
    forms_router = APIRouter()

    __register_form_routes(
        router=forms_router,
        form_internal_name='event-participation',
        form_pretty_name='Participation in Events',
        form_operation_name='FormEventParticipation',
        form_abbreviation_name='EP',
        form_model=EventParticipationForm,
        form_create_model=EventParticipationFormCreate,
        form_db_model=AlchemyEventParticipationFormModel,
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
        router=forms_router,
        form_internal_name='event-organization',
        form_pretty_name='Organization of Events',
        form_operation_name='FormEventOrganization',
        form_abbreviation_name='EO',
        form_model=EventOrganizationForm,
        form_create_model=EventOrganizationFormCreate,
        form_db_model=AlchemyEventOrganizationFormModel,
        allowed_sorts=[
            'user',
            'eventType',
            'involvementType',
            'designation',
            'participants',
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
        router=forms_router,
        form_internal_name='extension',
        form_pretty_name='Extension',
        form_operation_name='FormExtension',
        form_abbreviation_name='E',
        form_model=ExtensionForm,
        form_create_model=ExtensionFormCreate,
        form_db_model=AlchemyExtensionFormModel,
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
        router=forms_router,
        form_internal_name='supervision',
        form_pretty_name='Supervision',
        form_operation_name='FormSupervision',
        form_abbreviation_name='S',
        form_model=SupervisionForm,
        form_create_model=SupervisionFormCreate,
        form_db_model=AlchemySupervisionFormModel,
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

    __register_form_routes(
        router=forms_router,
        form_internal_name='jury-sci-committee',
        form_pretty_name='Jury Scientific Committee',
        form_operation_name='FormJuryScientificCommitee',
        form_abbreviation_name='JSC',
        form_model=JuryScientificCommitteeForm,
        form_create_model=JuryScientificCommitteeFormCreate,
        form_db_model=AlchemyJuryScientificCommitteeFormModel,
        allowed_sorts=[
            'user',
            'type',
            'dateStart'
        ],
        search_fields=[
            'user',
            'type'
        ]
    )

    __register_form_routes(
        router=forms_router,
        form_internal_name='referring-editorial-act',
        form_pretty_name='Refereeing Editorial Act',
        form_operation_name='FormRefereeingEditorialAct',
        form_abbreviation_name='REA',
        form_model=ReferringEditorialActForm,
        form_create_model=ReferringEditorialActFormCreate,
        form_db_model=AlchemyReferringEditorialActFormModel,
        allowed_sorts=[
            'user',
            'type',
            'regionType',
            'publicationType',
            'reviews',
            'year'
        ],
        search_fields=[
            'user',
            'type',
            'regionType',
            'publicationType'
        ]
    )

    router.include_router(
        forms_router,
        prefix="/forms"
    )


def __register_form_routes(
        router: APIRouter,
        form_internal_name: str,
        form_pretty_name: str,
        form_operation_name: str,
        form_abbreviation_name: str,
        form_model: Form,
        form_create_model: Form,
        form_db_model: AlchemyFormModel,
        allowed_sorts: List[str] = [],
        search_fields: List[str] = []
):
    @router.post(
        f"/{form_internal_name}",
        response_model=form_model,
        tags=[form_operation_name],
        status_code=status.HTTP_201_CREATED,
        summary=f'Create "{form_pretty_name}" form',
        operation_id=f'create{form_abbreviation_name}',
        description=f'Create new "{form_pretty_name}" form',
        response_description="The created form"
    )
    async def formCreate(
            form: form_create_model,
            user: User = Depends(controllers.user.get_current_user),
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

    @router.get(
        f"/{form_internal_name}/{{id:uuid}}",
        response_model=form_model,
        tags=[form_operation_name],
        summary=f'Get "{form_pretty_name}" form',
        operation_id=f'get{form_abbreviation_name}',
        description=f'Get "{form_pretty_name}" form by id',
        response_description="The requested form"
    )
    async def formGet(
            id: UUID4,
            user: User = Depends(controllers.user.get_current_superuser),
            db: Session = Depends(get_database)
    ):
        db_form = db.query(form_db_model).filter(form_db_model.id == id).first()
        if db_form is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return db_form

    @router.patch(
        f"/{form_internal_name}/{{id:uuid}}",
        response_model=form_model,
        tags=[form_operation_name],
        summary=f'Update "{form_pretty_name}" form',
        operation_id=f'update{form_abbreviation_name}',
        description=f'Update "{form_pretty_name}" form by id',
        response_description="The updated form"
    )
    async def formUpdate(
            id: UUID4,
            form: form_create_model,
            user: User = Depends(controllers.user.get_current_user),
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

    @router.delete(
        f"/{form_internal_name}/{{id:uuid}}",
        tags=[form_operation_name],
        status_code=status.HTTP_204_NO_CONTENT,
        summary=f'Delete "{form_pretty_name}" form',
        operation_id=f'delete{form_abbreviation_name}',
        description=f'Delete "{form_pretty_name}" form by id'
    )
    async def formDelete(
            id: UUID4,
            user: User = Depends(controllers.user.get_current_user),
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
        query = query.join(AlchemyUserModel, AlchemyUserModel.id == form_db_model.userId)

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

        return FormList[form_model](forms=forms, total=total)

    @router.get(
        f"/{form_internal_name}/list/me",
        response_model=FormList[form_model],
        tags=[form_operation_name],
        summary=f'Me "{form_pretty_name}" forms',
        operation_id=f'getAll{form_abbreviation_name}Me',
        description=f'Get the current user "{form_pretty_name}" forms',
        response_description="The user forms"
    )
    async def formListMe(
            size: int,
            page: int,
            date_from: Optional[date] = None,
            date_to: Optional[date] = None,
            sort: Optional[str] = None,
            desc: Optional[str] = None,
            q: Optional[str] = Query(None, min_length=3),
            user: User = Depends(controllers.user.get_current_user),
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

    @router.get(
        f"/{form_internal_name}/list",
        response_model=FormList[form_model],
        tags=[form_operation_name],
        summary=f'Get all "{form_pretty_name}" forms',
        operation_id=f'getAll{form_abbreviation_name}',
        description=f'Get all the "{form_pretty_name}" forms',
        response_description="The requested forms"
    )
    async def formList(
            size: int,
            page: int,
            date_from: Optional[date] = None,
            date_to: Optional[date] = None,
            sort: Optional[str] = None,
            desc: Optional[str] = None,
            q: Optional[str] = Query(None, min_length=3),
            user: User = Depends(controllers.user.get_current_superuser),
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

    @router.post(
        f"/{form_internal_name}/exports",
        response_model=ExportSchema,
        tags=[f'{form_operation_name}Schemas'],
        summary=f'Create "{form_pretty_name}" form schema',
        operation_id=f'create{form_abbreviation_name}Schema',
        description=f'Create a new "{form_pretty_name}" form schema',
        response_description="The created schema"
    )
    async def exportsCreate(
            export: ExportSchemaCreate,
            user: User = Depends(controllers.user.get_current_superuser),
            db: Session = Depends(get_database)
    ):

        created_export = AlchemyExportSchemaModel(
            **export.create_dict(),
            userId=user.id,
            type=form_internal_name
        )

        db.add(created_export)
        db.commit()
        db.refresh(created_export)

        return created_export

    @router.patch(
        f"/{form_internal_name}/exports/{{id:uuid}}",
        response_model=ExportSchema,
        tags=[f'{form_operation_name}Schemas'],
        summary=f'Update "{form_pretty_name}" form schema',
        operation_id=f'update{form_abbreviation_name}Schema',
        description=f'Update a "{form_pretty_name}" form schema by id',
        response_description="The updated schema"
    )
    async def exportsUpdate(
            id: UUID4,
            export: ExportSchemaCreate,
            user: User = Depends(controllers.user.get_current_superuser),
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

    @router.delete(
        f"/{form_internal_name}/exports/{{id:uuid}}",
        tags=[f'{form_operation_name}Schemas'],
        status_code=status.HTTP_204_NO_CONTENT,
        summary=f'Delete "{form_pretty_name}" form schema',
        operation_id=f'delete{form_abbreviation_name}Schema',
        description=f'Delete a "{form_pretty_name}" form schema by id'
    )
    async def exportsDelete(
            id: UUID4,
            user: User = Depends(controllers.user.get_current_superuser),
            db: Session = Depends(get_database)
    ):

        schema = db.query(AlchemyExportSchemaModel).filter(AlchemyExportSchemaModel.id == id).first()
        if schema is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        db.query(AlchemyExportSchemaModel).filter(AlchemyExportSchemaModel.id == id).delete()
        db.commit()

        return schema

    @router.get(
        f"/{form_internal_name}/exports/list",
        response_model=ExportSchemaList,
        tags=[f'{form_operation_name}Schemas'],
        summary=f'Get all "{form_pretty_name}" form schemas',
        operation_id=f'getAll{form_abbreviation_name}Schemas',
        description=f'Get all "{form_pretty_name}" form schemas',
        response_description="The requested schemas"
    )
    async def exportsList(
            user: User = Depends(controllers.user.get_current_superuser),
            db: Session = Depends(get_database)
    ):

        schemas = db.query(AlchemyExportSchemaModel).filter(AlchemyExportSchemaModel.type == form_internal_name).all()
        return ExportSchemaList(schemas=schemas)
