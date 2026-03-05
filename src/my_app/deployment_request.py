from pydantic import BaseModel


class DeploymentRequest(BaseModel):
    db_name: str = "matmon25-***"
    username: str
