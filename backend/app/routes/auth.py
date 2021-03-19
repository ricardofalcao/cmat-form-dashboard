from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.router.common import ErrorCode


def register_auth_routes(router: APIRouter, fastapi_users: FastAPIUsers, jwt_authentication: JWTAuthentication):
    auth_router = APIRouter();

    @auth_router.post("/login")
    async def login(
            response: Response, credentials: OAuth2PasswordRequestForm = Depends()
    ):
        user = await fastapi_users.db.authenticate(credentials)

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )

        return await jwt_authentication.get_login_response(user, response)

    router.include_router(
        auth_router,
        prefix="/auth/jwt"
    )
