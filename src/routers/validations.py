from src.my_exceptions.checking_deployment_exception import CheckingDeploymentException
from src.my_exceptions.validate_with_auth_exception import ValidateWithAuthException


def check_auth(login_username: str, input_username: str):
    if input_username != login_username:
        raise ValidateWithAuthException(f"The logged in username '{login_username}'"
                                              f" does not match the one in storage - '{input_username}'.")

def validate_db_name(db_name: str):
    if ' ' in db_name:
        raise CheckingDeploymentException("The db_name should not contain spaces.")
    if not db_name.startswith("matmon25-"):
        raise CheckingDeploymentException("Database must start with 'matmon25-'")


def validate_username(username: str):
    if ' ' in username:
        raise CheckingDeploymentException("The username should not contain spaces.")
    if not len(username) >= 3:
        raise CheckingDeploymentException("Username must be at least 3 characters.")


def validate_deployment(db_name: str, username: str):
    validate_db_name(db_name)
    validate_username(username)
