"""Defining the user manager"""
from fastapi import HTTPException
from passlib.context import CryptContext
from asyncpg import UniqueViolationError
from db import database
from managers.auth import AuthManager
from models import user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    """This UserManager registers the user
    saves it into the database, passes it to the
    authentication manager
    """
    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd_context.hash(user_data["password"])
        # In case a user is already registered
        try:
            id_ = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "User with this email already exists")
        user_do = await database.fetch_one(user.select().where(user.c.id == id_))
        return AuthManager.encode_token(user_do)
