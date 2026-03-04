from abc import ABC, abstractmethod


class CrudOnStorageTechnology(ABC):
    @abstractmethod
    def create_db(self):
        raise NotImplementedError

    @abstractmethod
    def read_db(self):
        raise NotImplementedError

    @abstractmethod
    def update_db(self):
        raise NotImplementedError

    @abstractmethod
    def delete_db(self):
        raise NotImplementedError
