from src.my_app.my_rest import MyApp

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
