import datetime
from uuid import UUID

import sqlalchemy as alc
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker

from src.postgres_files.deployment_table import DeploymentTable, Base
from src.my_exceptions.delete_deployment_exception import DeleteDeploymentException
from src.my_exceptions.deployment_doesnt_exist_exception import DeploymentDoesntExistException
from src.my_exceptions.deployment_exist_exception import DeploymentExistException
from src.postgres_files.user_model import User
from src.postgres_files.users_table import UsersTable
from src.request.deployment_request import DeploymentRequest
from src.postgres_files.status_type import StatusType


class PostgresConnection:
    def __init__(self):
        self.engine = alc.create_engine(
            "postgresql+psycopg2://{}:{}@{}/{}".format("postgres", "postgres", "localhost:5432", "postgres"))
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_new_user(self, user: User):
        self.get_deployment_by_id(user.deployment_id)
        with self.Session() as session:
            user = UsersTable(
                username=user.username,
                password=user.password,
                permission_level=user.permission_level,
                deployment_id=user.deployment_id
            )
            session.add(user)
            session.commit()


    def check_if_deployment_exist(self, db_name: str, username: str):
        with self.Session() as session:
            select_stmt = select(DeploymentTable).filter(DeploymentTable.db_name == db_name).filter(
                DeploymentTable.username == username).order_by(DeploymentTable.creation_time.desc())
            result = session.execute(select_stmt).scalars().first()
        if result is not None and result.status.name != StatusType.DELETED.name:
            raise DeploymentExistException("The deployment already exists.")

    def create_new_deployment(self, deployment: DeploymentRequest) -> str:
        with self.Session() as session:
            deployment = DeploymentTable(
                db_name=deployment.db_name,
                status="CREATED",
                username=deployment.username,
                creation_time=datetime.datetime.now()
            )
            session.add(deployment)
            session.commit()

            result = session.query(DeploymentTable).order_by(DeploymentTable.creation_time.desc()).first()

        return str(result.id)

    def get_deployment_by_id(self, deployment_id: UUID) -> dict:
        with self.Session() as session:
            select_stmt = select(DeploymentTable).filter(DeploymentTable.id == deployment_id)
            result = session.execute(select_stmt)
            result = result.scalars().first()
        if result:
            return {"id": result.id, "db_name": result.db_name, "status": result.status.name,
                    "creation_time": result.creation_time, "username": result.username}
        raise DeploymentDoesntExistException(f"Deployment id '{deployment_id}' was not found in the deployments table.")

    def update_db_name(self, deployment_id: UUID, new_db_name: str) -> None:
        result = self.get_deployment_by_id(deployment_id)
        if result.get("status") == StatusType.DELETED.name:
            raise DeleteDeploymentException("The deployment is unavailable - deleted.")
        with self.Session() as session:
            update_stmt = (
                update(DeploymentTable)
                .where(DeploymentTable.id == deployment_id)
                .values(db_name=new_db_name)
            )
            session.execute(update_stmt)
            session.commit()

    def delete_deployment(self, deployment_id: UUID, username: str) -> None:
        result = self.get_deployment_by_id(deployment_id)
        if result.get("status") == StatusType.DELETED.name:
            raise DeleteDeploymentException("The deployment is unavailable - deleted.")
        if result.get("username") == username:
            with self.Session() as session:
                delete_stmt = (
                    update(DeploymentTable)
                    .where(DeploymentTable.id == deployment_id)
                    .where(DeploymentTable.username == username)
                    .values(status="DELETED")
                )
                session.execute(delete_stmt)
                session.commit()
        else:
            raise DeleteDeploymentException(f"Username '{username}' does not match the admin details of the deployment.")

    def get_db_name_by_id(self, deployment_id: UUID):
        with self.Session() as session:
            select_stmt = (
                select(DeploymentTable)
                .where(DeploymentTable.id == deployment_id)
            )
            result = session.execute(select_stmt)

        if result:
            return session.execute(select_stmt).scalar().db_name
        raise DeploymentDoesntExistException(
            f"Deployment id '{deployment_id}' was not found in the deployments table.")

    def get_db_name_by_id_and_username(self, deployment_id: UUID, username: str) -> str:
        result = self.get_deployment_by_id(deployment_id)
        if result.get("status") == StatusType.DELETED.name:
            raise DeleteDeploymentException("The deployment is unavailable - deleted.")
        with self.Session() as session:
            select_stmt = (
                select(DeploymentTable)
                .where(DeploymentTable.id == deployment_id)
                .where(DeploymentTable.username == username)
            )
            result = session.execute(select_stmt).scalar()

        if result:
            return result.db_name
        raise DeploymentDoesntExistException(
            f"Deployment id '{deployment_id}' and username '{username}' was not found in the deployments table.")
