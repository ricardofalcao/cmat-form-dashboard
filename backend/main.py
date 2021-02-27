from fastapi import FastAPI, Depends, Query, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.router import ErrorCode
from fastapi_users.user import UserAlreadyExists
from starlette import status
from tortoise.contrib.fastapi import register_tortoise

from database import user_db
from models.user import User, UserCreate, UserUpdate, UserDB, UserList, TortoiseUserModel
from routes.auth import register_auth_routes
from routes.form import register_form_routes
from routes.user import register_user_routes

app = FastAPI()

#
#
#

JWT_SECRET = "M5Y8Q^uFD8Exs%h7"

auth_backends = []
jwt_authentication = JWTAuthentication(secret=JWT_SECRET, lifetime_seconds=12 * 60 * 60)
auth_backends.append(jwt_authentication)

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

#
#
#

DATABASE_URL = "sqlite://../test.db"

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["models.user", "aerich.models"],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["models.user", "models.forms"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

#
#
#

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:8000",
        "http://192.168.1.153",
        "http://192.168.1.153:8080",
        "http://192.168.1.153:8000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()
register_auth_routes(api_router, fastapi_users, jwt_authentication)
register_user_routes(api_router, fastapi_users)
register_form_routes(api_router, fastapi_users)

app.include_router(
    api_router,
    prefix="/api",
    tags=["api"]
)