from src.CRUD.crud_abc import CrudOnStorageTechnology
import pymongo

from src.postgress_connection import PostgresConnection


class MongoCrud(CrudOnStorageTechnology):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://nraboy:password1234@localhost:27017/")
        super().__init__()
        self.postgres_connection = PostgresConnection()

    def create_db(self, db_name: str, username: str) -> str:
        new_db = self.client[db_name]
        new_db[username].insert_one({"created": db_name})
        print(self.client.list_database_names())

    def read_db(self, deployment_id: str) -> dict:
        pass

    def update_db(self, deployment_id: str, db_new_name: str):
        for coll in self.client["temp"].list_collection_names():
            self.client[db_new_name][coll]
            for record in self.client["temp"][coll].find():
                a = self.client[db_new_name][coll].insert_one(record)
        self.client.drop_database("temp")

    def delete_db(self, deployment_id: str, username: str):
        self.postgres_connection.get_deployment_by_id(deployment_id)
        if
        self.client.drop_database("temp")
