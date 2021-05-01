from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routes.auth import register_auth_routes
from routes.form import register_form_routes
from routes.user import register_user_routes

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_PREFIX}/openapi.json',
    docs_url="/docs",
    redoc_url="/redoc"
)

#
#
#

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()
register_auth_routes(api_router)
register_user_routes(api_router)
register_form_routes(api_router)

app.include_router(api_router, prefix=settings.API_PREFIX)
