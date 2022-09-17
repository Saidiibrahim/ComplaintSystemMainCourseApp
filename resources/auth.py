"""This module is responsible for our authentication and registration"""
from fastapi import APIRouter

from managers.user import UserManager
from schemas.request.user import UserRegisterIn, UserLoginIn

router = APIRouter(tags=["Auth"])


# The URL for the register endpoint
@router.post("/register", status_code=201)
async def register(user_data: UserRegisterIn):  # user_data is all the data needed to create new users into the database
    token = UserManager.register(user_data)
    # User registers, the token should be returned because it's already encoded
    return {"token": token}


# Endpoint for logging in
@router.post("/login")
async def login(user_data: UserLoginIn):  # pass the user data because we're going to have it in the request
    # Accept the token from UserManager. UserManager has the logic to
    # check that there is such a user and that this is the correct password for this user
    token = UserManager.login(user_data)
    return {"token": token}

