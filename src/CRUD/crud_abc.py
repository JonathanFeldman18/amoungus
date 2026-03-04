from abc import ABC, abstractmethod


class CrudOnStorageTechnology(ABC):

    @abstractmethod
    def create_db(self, db_name: str, username: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def read_db(self, deployment_id: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def update_db(self, deployment_id: str, db_name: str):
        raise NotImplementedError

    @abstractmethod
    def delete_db(self, deployment_id: str, username: str):
        raise NotImplementedError
