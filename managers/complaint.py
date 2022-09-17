from db import database
from models import complaint, RoleType, State


class ComplaintManager:
    @staticmethod
    async def get_complaint(user):
        # q is query
        q = complaint.select()  # Select here means get all complaints
        # If user is a complainer
        if user["role"] == RoleType.complainer:
            # get only complaints related to this user. Not all complaints
            q = q.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            q = q.where(complaint.c.state == State.pending)
        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(complaint_data):
        # Create a new complaint in the database
        id_ = await database.execute(complaint.insert().values(complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))
