from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core import controllers, utils
from core.models.auth import AuthResponse
from db import get_database


def register_auth_routes(router: APIRouter):
    auth_router = APIRouter()

    @auth_router.post(
        "/login",
        response_model=AuthResponse,
        tags=['Auth'],
        summary='Login',
        operation_id='login',
        description='Login with a username and password',
        response_description="The generated access token"
    )
    async def login(
            credentials: OAuth2PasswordRequestForm = Depends(),
            db: Session = Depends(get_database)
    ):
        user = await controllers.user.authenticate_user(db, credentials)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad credentials",
            )

        token = utils.generate_token(user.id)
        return AuthResponse(access_token=token, token_type="bearer")

    router.include_router(
        auth_router,
        prefix="/auth/jwt"
    )
