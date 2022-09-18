from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from managers.auth import oauth2_schema, is_complainer
from managers.complaint import ComplaintManager
from schemas.response.complaint import ComplaintOut

router = APIRouter(tags=["Complaints"])


# The dependencies arg protects this route
@router.get("/complaints/", dependencies=[Depends(oauth2_schema)], response_model=List[ComplaintOut])
async def get_complaints(request: Request):
    user = request.state.user
    # get_complaint is async and goes to database, so needs to be awaited
    return await ComplaintManager.get_complaint(user)


@router.post("/complaints/", dependencies=[Depends(oauth2_schema), Depends(is_complainer)], response_model=ComplaintOut)
async def create_complaint(complaint: ComplaintOut):
    return await ComplaintManager.create_complaint(complaint.dict())  # the complaint as a dict. Remember from the
    # login and register part
