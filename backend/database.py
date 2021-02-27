from fastapi_users.db import TortoiseUserDatabase

from models.user import UserDB, TortoiseUserModel

user_db = TortoiseUserDatabase(UserDB, TortoiseUserModel)