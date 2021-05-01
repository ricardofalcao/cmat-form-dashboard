from typing import List, Optional

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status

from core import controllers
from db import get_database
from core.models import UserList, User, UserCreate, AlchemyUserModel, UserUpdate, UUID4, UserDB


async def _get_or_404(db: Session, id: UUID4) -> UserDB:
    user = await controllers.user.get_user_by_id(db, id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


def register_user_routes(router: APIRouter):
    users_router = APIRouter()

    """
    Get current user
    """

    @users_router.get(
        "/me",
        response_model=User,
        tags=['User'],
        summary='Get Me',
        operation_id='getUserMe',
        description='Get current user',
        response_description="The authenticated user"
    )
    async def me(
            user: User = Depends(controllers.user.get_current_user),
    ):
        return user

    """
    Update current user
    """

    @users_router.patch(
        "/me",
        response_model=User,
        tags=['User'],
        summary='Update Me',
        operation_id='updateUserMe',
        description='Update current user',
        response_description="Update the authenticated user"
    )
    async def update_me(
            update: UserUpdate,
            db: Session = Depends(get_database),
            user: User = Depends(controllers.user.get_current_user),
    ):
        for key, value in update.update_dict().items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return user

    """
    Get user by id
    """

    @users_router.get(
        "/{id:uuid}",
        response_model=User,
        tags=['User'],
        summary='Get User',
        operation_id='getUser',
        description='Get User by Id',
        response_description="The requested user"
    )
    async def get_user(
            id: UUID4,
            db: Session = Depends(get_database),
            user: User = Depends(controllers.user.get_current_superuser)
    ):
        return await _get_or_404(db, id)

    """
    Update user by id
    """

    @users_router.patch(
        "/{id:uuid}",
        response_model=User,
        tags=['User'],
        summary='Update User',
        operation_id='updateUser',
        description='Update User by Id',
        response_description="The updated user"
    )
    async def update_user(
            id: UUID4,
            update: UserUpdate,
            db: Session = Depends(get_database),
            superuser: User = Depends(controllers.user.get_current_superuser)
    ):
        user = await _get_or_404(id)

        for key, value in update.update_dict().items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return user

    """
    Delete user by id
    """

    @users_router.delete(
        "/{id:uuid}",
        tags=['User'],
        summary='Delete User',
        operation_id='deleteUser',
        description='Delete User by Id',
        status_code=status.HTTP_204_NO_CONTENT
    )
    async def delete_user(
            id: UUID4,
            db: Session = Depends(get_database),
            superuser: User = Depends(controllers.user.get_current_superuser)
    ):
        user = await _get_or_404(id)
        await controllers.user.delete_user(db, user)
        return None

    """
    Search users by query
    """

    @users_router.get(
        "/search",
        response_model=UserList,
        tags=['User'],
        summary="Search Users",
        operation_id='searchUsers',
        description="Search for users based on a name query",
        response_description="The users matching the query"
    )
    async def users_list(
            q: Optional[List[str]] = Query(None),
            db: Session = Depends(get_database),
            user: User = Depends(controllers.user.get_current_user),
    ):
        conds = []

        for name in q:
            conds.append(AlchemyUserModel.name.contains(name))

        query = db.query(AlchemyUserModel).filter(or_(*conds)).all()

        return {
            "users": query
        }

    """
    List all registered users
    """

    @users_router.get(
        "/list",
        response_model=UserList,
        tags=['User'],
        summary="Get all Users",
        operation_id='getAllUsers',
        description="Get all users registered in the database",
        response_description="The users"
    )
    async def users_list(
            user: User = Depends(controllers.user.get_current_superuser),
            db: Session = Depends(get_database)
    ):
        query = db.query(AlchemyUserModel).all()
        return UserList(users=query)

    """
    Create new user
    """

    @users_router.post(
        "/create",
        response_model=User,
        tags=['User'],
        status_code=status.HTTP_201_CREATED,
        summary="Create User",
        operation_id='createUser',
        description="Create a new user in the database",
        response_description="The created user"
    )
    async def register(
            user: UserCreate,
            superuser: User = Depends(controllers.user.get_current_superuser),
            db: Session = Depends(get_database)
    ):
        created_user = await controllers.user.create_user(db, user)
        return created_user

    router.include_router(
        users_router,
        prefix="/users"
    )
