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

    @staticmethod
    async def login(user_data):
        # Search the database for user with this email
        user_do = await database.fetch_one(user.select().where(user.c.email == user_data["email"]))
        # If the user doesn't exist in database
        if not user_do:
            raise HTTPException(400, "wrong email or password")  # Because we don't want to say we don't have this user
        # Or if the password is wrong
        elif not pwd_context.verify(user_data["password"], user_data["password"]):
            # For security reasons, if password is wrong, we return the same message
            # This way we don't expose sensitive information.
            # If we say we don't have this user, that's not only informative to the user,
            # but also to the hackers as well
            raise HTTPException(400, "wrong email or password")
        # If we have the user and the password is correct,
        # return the encoded token for this user
        return AuthManager.encode_token(user_do)



