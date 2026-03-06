from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette.responses import JSONResponse

from src.CRUD.mongo_commands import MongocCommends
from src.my_exceptions.checking_deployment_exception import CheckingDeploymentException
from src.my_exceptions.deployment_exist_exception import DeploymentExistException
from src.my_exceptions.validate_with_auth_exception import ValidateWithAuthException
from src.requests.deployment_request import DeploymentRequest
from src.requests.update_db_name_request import UpdateDbNameRequest
from src.routers.validations import validate_db_name, validate_deployment, check_auth
from src.my_exceptions.deployment_doesnt_exist_exception import DeploymentDoesntExistException
from src.postgres_files.postgress_connection import PostgresConnection

router = APIRouter(prefix="/deployments", tags=["Deployments"])

security = HTTPBasic()

mongo_commands = MongocCommends()
postgres_connection = PostgresConnection()


# , credentials: Annotated[HTTPBasicCredentials, Depends(security)])


@router.post("/", tags=["Deployments"])
async def create_deployment(deployment: DeploymentRequest,
                            credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    db_name = deployment.db_name
    username = deployment.username
    try:
        check_auth(credentials.username, username)
        validate_deployment(db_name, username)
        postgres_connection.check_if_deployment_exist(db_name, username)
        deployment_id = postgres_connection.create_new_deployment(deployment)
        mongo_commands.create_db(db_name, username)
        return JSONResponse(status_code=201, content={"id": deployment_id})
    except (CheckingDeploymentException, DeploymentExistException, ValidateWithAuthException) as e:
        return JSONResponse(status_code=422, content={"Error": str(e)})


@router.get("/{deployment_id}", tags=["Deployments"])
async def get_deployment(deployment_id: UUID, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    try:
        deployment = postgres_connection.get_deployment_by_id(deployment_id)
        check_auth(credentials.username, deployment.pop("username"))
        return deployment
    except Exception as e:
        return JSONResponse(status_code=404, content={"Error": str(e)})


@router.put("/{deployment_id}", tags=["Deployments"])
async def update_deployment(deployment_id: UUID, update_db_name_request: UpdateDbNameRequest,
                            credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    new_db_name = update_db_name_request.new_db_name
    try:
        validate_db_name(new_db_name)
        deployment = postgres_connection.get_deployment_by_id(deployment_id)
        check_auth(credentials.username, deployment.get("username"))
        mongo_commands.update_db(deployment.get("db_name"), new_db_name)
        postgres_connection.update_db_name(deployment_id, new_db_name)
        return JSONResponse(status_code=200, content={"id": str(deployment_id)})
    except (CheckingDeploymentException, DeploymentDoesntExistException, ValidateWithAuthException) as e:
        return JSONResponse(status_code=422, content={"Error": str(e)})


@router.delete("/{deployment_id}", tags=["Deployments"])
async def delete_deployment(deployment_id: UUID, username: str,
                            credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    try:
        check_auth(credentials.username, username)
        postgres_connection.delete_deployment(deployment_id, username)
        mongo_commands.delete_db(deployment_id, username)
        return JSONResponse(status_code=204, content={"message": "Deleted successfully"})
    except Exception as e:
        return JSONResponse(status_code=422, content={"Error": str(e)})


@router.get("/connection_string/", tags=["Deployments"])
async def get_deployment_connection_string(deployment_id: UUID, username: str,
                                           credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    try:
        check_auth(credentials.username, username)
        url = mongo_commands.get_url()
        url += postgres_connection.get_db_name_by_id_and_username(deployment_id, username)
        return JSONResponse(status_code=200, content={"connection_string": url})
    except Exception as e:
        return JSONResponse(status_code=404, content={"Error": str(e)})
