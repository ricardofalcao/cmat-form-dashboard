from datetime import datetime, timedelta

import jwt
from pydantic import UUID4

from config import settings

JWT_ALGORITHM = "HS256"


def _generate_jwt(
        data: dict, lifetime_seconds: int, secret: str, algorithm: str = JWT_ALGORITHM
) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=lifetime_seconds)
    payload["exp"] = expire
    return jwt.encode(payload, secret, algorithm=algorithm)


def generate_token(user_id: UUID4) -> str:
    data = {"user_id": str(user_id), "aud": "cmatforms:auth"}
    return _generate_jwt(data, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, settings.SECRET_KEY, JWT_ALGORITHM)


def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM], audience="cmatforms:auth")

        user_id = payload.get("user_id")
        if user_id is None:
            return None

        user_uiid = UUID4(user_id)
        return user_uiid
    except jwt.PyJWTError:
        return None
