from pydantic import BaseModel


class UpdateDbNameRequest(BaseModel):
    new_db_name: str
