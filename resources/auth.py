"""This module is responsible for our authentication and registration"""
from fastapi import APIRouter

from managers.user import UserManager

router = APIRouter(tags=["Auth"])


# The URL for the register endpoint
@router.post("/register", status_code=201)
async def register(user_data):  # user_data is all the data needed to create new users into the database
    token = UserManager.register(user_data)
    # User registers, the token should be returned because it's already encoded
    return {"token": token}
