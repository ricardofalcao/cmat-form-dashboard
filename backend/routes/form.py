from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers, models
from pydantic import UUID4
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
        AlchemyEventParticipationFormModel
    )

    __register_form_routes(
        forms_router,
        fastapi_users,
        'event-organization',
        EventOrganizationForm,
        EventOrganizationFormCreate,
        AlchemyEventOrganizationFormModel
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
        form_db_model: AlchemyModel
):
    class FormList(models.BaseModel):
        forms: List[form_model]

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
            user: User = Depends(fastapi_users.current_user(superuser=True)),
            db: Session = Depends(get_database)
    ):
        db_form = db.query(form_db_model).filter(form_db_model.id == id).first()
        if db_form is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        db.query(form_db_model).filter(id=id).delete()
        db.commit()

        return None

    @router.get(f"/{form_name}/list", response_model=FormList)
    async def formList(
            user: User = Depends(fastapi_users.current_user(superuser=True)),
            db: Session = Depends(get_database)
    ):
        db_forms = db.query(form_db_model).all()

        return FormList(forms=db_forms)
