from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette import status

from config import settings
from db import get_database
from core.models import UserDB, AlchemyUserModel, UserCreate, User
from core.utils import password, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/jwt/login")


async def get_current_user(
        db: Session = Depends(get_database),
        token: str = Depends(oauth2_scheme)
) -> User:
    user_id = jwt.decode_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_by_id(db, id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_superuser(user: User = Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate superuser status"
        )

    return user


async def get_user_by_id(db: Session, id: UUID4) -> UserDB:
    res = db.query(AlchemyUserModel).filter(AlchemyUserModel.id == id).first()
    return res


async def get_user_by_email(db: Session, email: str) -> UserDB:
    res = db.query(AlchemyUserModel).filter(AlchemyUserModel.email == email).first()
    return res


async def create_user(db: Session, user: UserCreate) -> UserDB:
    created_form = UserDB(
        **user.create_dict()
    )

    db.add(created_form)
    db.refresh(created_form)
    return created_form

async def delete_user(db: Session, user: User):
    db.query(AlchemyUserModel.id == user.id).delete()
    db.commit()

async def authenticate_user(db: Session, credentials: OAuth2PasswordRequestForm):
    """
    Authenticate and return a user following an email and a password.

    Will automatically upgrade password hash if necessary.
    """

    user = await get_user_by_email(db, credentials.username)

    if user is None:
        # Run the hasher to mitigate timing attack
        # Inspired from Django: https://code.djangoproject.com/ticket/20760
        password.get_password_hash(credentials.password)
        return None

    verified, updated_password_hash = password.verify_and_update_password(
        credentials.password, user.hashed_password
    )
    if not verified:
        return None
    # Update password hash to a more robust one if needed
    if updated_password_hash is not None:
        user.hashed_password = updated_password_hash
        await db.commit()

    return user
