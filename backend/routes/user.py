from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users.router import ErrorCode
from fastapi_users.user import UserAlreadyExists
from sqlalchemy.orm import Session
from starlette import status

from database import get_database
from models.user import UserList, User, UserDB, UserCreate, AlchemyUserModel


def register_user_routes(router: APIRouter, fastapi_users: FastAPIUsers):
    users_router = fastapi_users.get_users_router()

    @users_router.get("/search", response_model=UserList)
    async def users_list(
            q: str = Query(..., min_length=3, max_length=64),
            user: User = Depends(fastapi_users.current_user()),
            db: Session = Depends(get_database)
    ):
        query = db.query(AlchemyUserModel).filter(AlchemyUserModel.name.contains(q)).all()

        return {
            "users": query
        }

    @users_router.get("/list", response_model=UserList)
    async def users_list(
            user: User = Depends(fastapi_users.current_user(superuser=True)),
            db: Session = Depends(get_database)
    ):
        query = db.query(AlchemyUserModel).all()
        return UserList(users=query)

    @users_router.post("/create", response_model=User, status_code=status.HTTP_201_CREATED)
    async def register(
            user: UserCreate,
            superuser: User = Depends(fastapi_users.current_user(superuser=True)),
    ):
        try:
            created_user = await fastapi_users.create_user(user, safe=True)
        except UserAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
            )

        return created_user

    router.include_router(
        users_router,
        prefix="/users"
    )
