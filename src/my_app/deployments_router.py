from uuid import UUID

from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.CRUD.mongo_commands import MongocCommends
from src.request.deployment_request import DeploymentRequest
from src.request.update_db_name_request import UpdateDbNameRequest
from src.my_app.validation import validate_db_name, validate_deployment
from src.my_exceptions.deployment_doesnt_exist_exception import DeploymentDoesntExistException
from src.postgres_files.postgress_connection import PostgresConnection

router = APIRouter(prefix="/deployments", tags=["deployments"])

mongo_commands = MongocCommends()
postgres_connection = PostgresConnection()


@router.post("/{db_name: str, username: str}", tags=["deployments"])
async def add_deployment(deployment: DeploymentRequest):
    db_name = deployment.db_name
    username = deployment.username
    try:
        if validate_deployment(db_name, username):
            result = postgres_connection.check_if_deployment_exist(db_name, username)
            if result is None:
                deployment_id = postgres_connection.create_new_deployment(deployment)
                mongo_commands.create_db(db_name, username)
                return JSONResponse(status_code=201, content={"id": deployment_id})
    except Exception as e:
        return JSONResponse(status_code=422, content={"Error": str(e)})


@router.get("/:<deployment_id> ", tags=["deployments"])
async def get_deployment(deployment_id: UUID):
    try:
        result = postgres_connection.get_deployment_by_id(deployment_id)
        result.pop("username")
        return result
    except DeploymentDoesntExistException as e:
        JSONResponse(status_code=404, content={"Error": str(e)})


@router.put("/:deployment_id", tags=["deployments"])
async def update_db_name(deployment_id: UUID, update_db_name_request: UpdateDbNameRequest):
    new_db_name = update_db_name_request.new_db_name
    try:
        if validate_db_name(new_db_name):
            mongo_commands.update_db(postgres_connection.get_db_name_by_id(deployment_id),
                                     update_db_name_request.new_db_name)
            postgres_connection.update_db_name(deployment_id, update_db_name_request.new_db_name)
            return JSONResponse(status_code=200, content={"id": str(deployment_id)})
    except Exception as e:
        return JSONResponse(status_code=422, content={"Error": str(e)})


@router.delete("/:<deployment_id>", tags=["deployments"])
async def delete_deployment(deployment_id: UUID, username: str):
    try:
        postgres_connection.delete_deployment(deployment_id, username)
        mongo_commands.delete_db(deployment_id, username)
        return JSONResponse(status_code=201, content="")
    except Exception as e:
        return JSONResponse(status_code=422, content={"Error": str(e)})


@router.get("/connection_string/:<deployment_id>", tags=["deployments"])
async def get_connection_string(deployment_id: UUID, username: str):
    try:
        url = mongo_commands.get_url()
        url += postgres_connection.get_db_name_by_id_and_username(deployment_id, username)
        return JSONResponse(status_code=200, content={"connection_string": url})
    except Exception as e:
        return JSONResponse(status_code=404, content={"Error": str(e)})
