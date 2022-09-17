"""This is the starting point of our application"""

from fastapi import FastAPI

from db import database
from resources.routes import api_router

app = FastAPI()
app.include_router(api_router)  # This is how the main app knows about the routers


# Configure before start and after shutdown
@app.on_event("startup")
async def startup():
    # On startup, connect to database
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
