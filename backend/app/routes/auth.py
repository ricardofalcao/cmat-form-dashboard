from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication


def register_auth_routes(router: APIRouter, fastapi_users: FastAPIUsers, jwt_authentication: JWTAuthentication):
    auth_router = APIRouter();

    auth_router.include_router(
        fastapi_users.get_auth_router(jwt_authentication),
        prefix="/jwt"
    )

    router.include_router(
        auth_router,
        prefix="/auth"
    )
