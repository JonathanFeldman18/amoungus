import datetime
from typing import Optional

import uvicorn
from fastapi import FastAPI
from sqlalchemy import String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

from src.CRUD.mongo_commands import MongocCommends
from src.my_app.deployment_request import DeploymentRequest
from src.my_app.my_rest import MyApp
import sqlalchemy as alc

from src.my_app.status_type import StatusType
from src.postgress_connection import PostgresConnection

if __name__ == '__main__':
    #postgres_connection = PostgresConnection()
    #postgres_connection.create_new_deployment(DeploymentRequest.model_validate({"db_name": "matmon25-fewfef", "username": "fewfef"}))
    #print(postgres_connection.get_deployment_by_id("019cba93-888d-720f-8b4a-343344e715a5"))
    #postgres_connection.get_db_name("019cbad8-b930-755e-8846-591c4c618a69", "fewfef")

    #mongo_connection = MongoCrud()
    #mongo_connection.create_db("temp", "temp4")
    #mongo_connection.update_db("deqwd", "temp1")
    #result = get_db()
    my_app = MyApp()
    my_app.run_my_app()
