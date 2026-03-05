from uuid import UUID

from src.CRUD.crud_abc import CrudOnStorageTechnology
import pymongo

from src.postgress_connection import PostgresConnection


class MongocCommends(CrudOnStorageTechnology):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://nraboy:password1234@localhost:27017/")
        super().__init__()
        self.postgres_connection = PostgresConnection()

    def get_url(self) -> str:
        return "mongodb://nraboy:password1234@localhost:27017/"

    def create_db(self, db_name: str, username: str):
        new_db = self.client[db_name]
        new_db[username].insert_one({"created": db_name})

    def read_db(self, deployment_id: UUID) -> dict:
        pass

    def update_db(self, old_db_name, new_db_name: str):
        for coll in self.client[old_db_name].list_collection_names():
            #self.client[new_db_name][coll]
            for record in self.client[old_db_name][coll].find():
                a = self.client[new_db_name][coll].insert_one(record)
        self.client.drop_database(old_db_name)

    def delete_db(self, deployment_id: UUID, username: str):
        db_name = self.postgres_connection.get_db_name_by_id(deployment_id)
        self.client[db_name][username].drop()
