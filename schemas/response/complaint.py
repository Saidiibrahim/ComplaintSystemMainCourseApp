from datetime import datetime

from schemas.base import BaseComplaint

from models import State


class ComplaintOut(BaseComplaint):
    id: int  # Should already be in database, should have an id
    created_at: datetime
    status: State
    