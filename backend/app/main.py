import os

import databases

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase

from dbase import Base, engine, DATABASE_URL

from models.user import User, UserCreate, UserUpdate, UserDB, AlchemyUserModel
from routes.auth import register_auth_routes
from routes.form import register_form_routes
from routes.user import register_user_routes

base_prefix = os.getenv("API_PREFIX", "")
app = FastAPI(root_path=base_prefix, docs_url="/docs", redoc_url="/redoc")

#
#
#

JWT_SECRET = "M5Y8Q^uFD8Exs%h7"

auth_backends = []
jwt_authentication = JWTAuthentication(secret=JWT_SECRET, lifetime_seconds=12 * 60 * 60)
auth_backends.append(jwt_authentication)

#
#
#


Base.metadata.create_all(bind=engine)

raw_database = databases.Database(DATABASE_URL)
fastapi_users = FastAPIUsers(
    SQLAlchemyUserDatabase(UserDB, raw_database, AlchemyUserModel.__table__),
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

#
#
#

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8080",
        "https://mat.ricardofalcao.pt"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = app.router
register_auth_routes(api_router, fastapi_users, jwt_authentication)
register_user_routes(api_router, fastapi_users)
register_form_routes(api_router, fastapi_users)

@app.on_event("startup")
async def startup():
    await raw_database.connect()


@app.on_event("shutdown")
async def shutdown():
    await raw_database.disconnect()
