import datetime

from pydantic import BaseModel

from src.status_type import StatusType


class Deployment(BaseModel):
    id: str
    db_name: str
    status: StatusType
    creation_time: datetime.datetime
