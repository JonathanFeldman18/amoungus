from pydantic import BaseModel


class UpdateDbNameRequest(BaseModel):
    db_name: str = "matmon25-***"
