from src.CRUD.mongo_crud import MongoCrud
from src.postgress_connection import PostgresConnection

if __name__ == '__main__':
    #postgres_connection = PostgresConnection()
    #postgres_connection.create_new_deployment()

    mongo_connection = MongoCrud()
    #mongo_connection.create_db("temp", "temp4")
    #mongo_connection.update_db("deqwd", "temp1")
