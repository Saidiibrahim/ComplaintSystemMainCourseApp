"""This file will be responsible for binding
all the existing routers to a simple router that
will be included in the main file"""
from fastapi import APIRouter
from resources import auth

api_router = APIRouter()
# Bind the router to an already existing router
api_router.include_router(auth.router)
