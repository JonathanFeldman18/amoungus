from abc import ABC, abstractmethod
from uuid import UUID


class CrudOnStorageTechnology(ABC):

    @abstractmethod
    def create_db(self, db_name: str, username: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def read_db(self, deployment_id: UUID) -> dict:
        raise NotImplementedError

    @abstractmethod
    def update_db(self, old_db_name, new_db_name: str):
        raise NotImplementedError

    @abstractmethod
    def delete_db(self, deployment_id: UUID, username: str):
        raise NotImplementedError
