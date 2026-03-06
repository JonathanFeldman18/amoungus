from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import JSONResponse

from src.CRUD.mongo_commands import MongocCommends
from src.my_exceptions.checking_deployment_exception import CheckingDeploymentException
from src.my_exceptions.delete_deployment_exception import DeleteDeploymentException
from src.my_exceptions.deployment_doesnt_exist_exception import DeploymentDoesntExistException
from src.my_exceptions.user_exist_exception import UserExistException
from src.my_exceptions.validate_password_exception import ValidatePasswordException
from src.my_exceptions.validate_with_auth_exception import ValidateWithAuthException
from src.postgres_files.postgress_connection import PostgresConnection
from src.requests.user_request import User
from src.routers.validations import validate_password, validate_username, validate_permission_level, check_full_auth

router = APIRouter(prefix="/users", tags=["Users"])

security = HTTPBasic()

mongo_commands = MongocCommends()
postgres_connection = PostgresConnection()


@router.post("/", tags=["Users"])
async def create_user(user: User, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    try:
        validate_password(user.password)
        validate_username(user.username)
        check_full_auth(credentials.username, user.username, credentials.password, user.password)
        validate_permission_level(user.permission_level)
        postgres_connection.check_if_user_exist(user.username)
        postgres_connection.create_new_user(user)
        return JSONResponse(status_code=201, content={"message": "The user has been successfully saved."})
    except (CheckingDeploymentException, ValidatePasswordException,
            DeploymentDoesntExistException, UserExistException,
            ValidateWithAuthException, DeleteDeploymentException) as e:
        return JSONResponse(status_code=422, content={"Error": str(e)})
