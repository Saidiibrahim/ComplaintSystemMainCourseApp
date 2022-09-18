from typing import Optional

import jwt
from datetime import datetime, timedelta
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from db import database
from models import user, RoleType


class AuthManager:
    """Responsible for everything related to authentication"""
    @staticmethod
    def encode_token(user):
        """
        Encodes a user's access token
        """
        try:
            payload = {
                "sub": user["id"],  # sub means subject
                "exp": datetime.utcnow() + timedelta(minutes=120)  # exp means expires
            }
            return jwt.encode(payload, config('SECRET_KEY'), algorithm='HS256')
        except Exception as ex:
            # Log the exception
            raise ex


class CustomHTTPBearer(HTTPBearer):
    """
    Customized HTTPBearer
    """
    # async def from HTTPBearer
    async def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super.__call__(request)
        # Extending it here
        try:
            payload = jwt.decode(res.credentials, config("SECRET_KEY"), algorithms=["HS256"])
            # Fetch the user from database
            user_data = await database.fetch_one(user.select().where(user.c.id == payload["sub"]))
            # Bind this to the request, so we have a global user for this response cycle
            request.state.user = user_data
            # return the user data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token is expired")  # 401 means unauthenticated
        # In the case the token is invalid
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Token is invalid")


# Authentication schema
oauth2_schema = CustomHTTPBearer()


def is_complainer(request):
    if not request.state.user["role"] == RoleType.complainer:
        raise HTTPException(403, "Forbidden")


def is_approver(request):
    if not request.state.user["role"] == RoleType.approver:
        raise HTTPException(403, "Forbidden")


def is_admin(request):
    if not request.state.user["role"] == RoleType.admin:
        raise HTTPException(403, "Forbidden")

