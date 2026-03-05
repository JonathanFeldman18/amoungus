import datetime

from pydantic import BaseModel

from src.my_app.status_type import StatusType


class Deployment(BaseModel):
    id: str
    db_name: str
    status: StatusType
    creation_time: datetime.datetime
