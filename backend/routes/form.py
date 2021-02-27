from fastapi import FastAPI, APIRouter, Query, Depends, HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.router import ErrorCode
from fastapi_users.user import UserAlreadyExists
from pydantic import UUID4
from starlette import status

from models.forms import EventParticipationForm, EventParticipationFormBase, EventParticipationFormCreate, \
    TortoiseEventParticipationFormModel, EventParticipationFormList
from models.user import UserList, User, TortoiseUserModel, UserDB, UserCreate


def register_form_routes(router: APIRouter, fastapi_users: FastAPIUsers):
    forms_router = APIRouter()

    @forms_router.post("/event-participation", response_model=EventParticipationForm,
                       status_code=status.HTTP_201_CREATED)
    async def eventParticipationCreate(
            form: EventParticipationFormCreate,
            user: User = Depends(fastapi_users.current_user()),
    ):
        created_form = await TortoiseEventParticipationFormModel.create(
            **form.dict(exclude_unset=True),
            user_id=user.id,
            date_start=form.date[0],
            date_finish=form.date[1],
        )
        await created_form.fetch_related('user')

        form_dict = await created_form.to_dict()
        user_dict = await created_form.user.to_dict()

        output = EventParticipationForm(**form_dict, user=User(**user_dict))
        return output

    @forms_router.get("/event-participation/{id:uuid}", response_model=EventParticipationForm)
    async def eventParticipationGet(
            id: UUID4,
            user: User = Depends(fastapi_users.current_user(superuser=True)),
    ):
        db_form = await TortoiseEventParticipationFormModel.filter(id = id).prefetch_related('user')
        if db_form is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        form_dict = await db_form.to_dict()
        user_dict = await db_form.user.to_dict()

        output = EventParticipationForm(**form_dict, user=User(**user_dict))
        return output

    @forms_router.delete("/event-participation/{id:uuid}", status_code=status.HTTP_204_NO_CONTENT)
    async def eventParticipationGet(
            id: UUID4,
            user: User = Depends(fastapi_users.current_user(superuser=True)),
    ):
        db_form = await TortoiseEventParticipationFormModel.get(id = id)
        if db_form is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        await TortoiseEventParticipationFormModel.filter(id = id).delete()

        return None

    @forms_router.get("/event-participation/list", response_model=EventParticipationFormList)
    async def eventParticipationGet(
            user: User = Depends(fastapi_users.current_user(superuser=True)),
    ):
        db_forms = await TortoiseEventParticipationFormModel.filter().prefetch_related('user').all()

        output = []
        for db_form in db_forms:
            form_dict = await db_form.to_dict()
            user_dict = await db_form.user.to_dict()

            output.append(EventParticipationForm(**form_dict, user=User(**user_dict)))

        return EventParticipationFormList(forms = output)

    router.include_router(
        forms_router,
        prefix="/forms"
    )
