from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from tortoise.contrib.fastapi import register_tortoise

from database import user_db
from models.user import User, UserCreate, UserUpdate, UserDB, UserList, TortoiseUserModel

app = FastAPI()

#
#
#

JWT_SECRET = "M5Y8Q^uFD8Exs%h7"

auth_backends = []
jwt_authentication = JWTAuthentication(secret=JWT_SECRET, lifetime_seconds=3600)
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
    modules={"models": ["models.user"]},
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
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(jwt_authentication),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"]
)

users_router = fastapi_users.get_users_router();


@users_router.get("/search", response_model=UserList)
async def users_list(
        q: str = Query(..., min_length=3, max_length=64)
        #        user: User = Depends(fastapi_users.current_user(active=True)),  # type: ignore
):
    query = TortoiseUserModel.filter(name__contains=q).all()
    users = await query

    output = []
    for user in users:
        user_dict = await user.to_dict()

        output.append(UserDB(**user_dict))

    return {
        "users": output
    }


app.include_router(
    users_router,
    prefix="/users",
    tags=["users"]
)
