from uuid import UUID

from pydantic import BaseModel

from src.postgres_files.permission_level import PermissionLevel


class User(BaseModel):
    username: str
    password: str
    permission_level: str = "read"
    deployment_id: UUID = "string"
