import re

from src.my_exceptions.checking_deployment_exception import CheckingDeploymentException
from src.my_exceptions.validate_password_exception import ValidatePasswordException
from src.my_exceptions.validate_with_auth_exception import ValidateWithAuthException


def check_auth(login_username: str, input_username: str):
    if input_username != login_username:
        raise ValidateWithAuthException(f"The logged in username '{login_username}'"
                                        f" does not match the one in storage - '{input_username}'.")


def check_full_auth(login_username: str, input_username: str, login_password: str, input_password: str):
    if input_username != login_username:
        raise ValidateWithAuthException(f"The logged in username '{login_username}'"
                                        f" does not match the one in storage - '{input_username}'.")
    if login_password != input_password:
        raise ValidateWithAuthException(f"The logged in password does not match the one in storage")


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


def validate_password(password: str):
    if len(password) < 8:
        raise ValidatePasswordException("The password must contain at least 8 characters.")
    if not re.search('[0-9]', password):
        raise ValidatePasswordException("The password must contain at least one digit.")
    if not re.search('[A-Z]', password):
        raise ValidatePasswordException("The password must contain at least one uppercase letter.")
    if not re.search('[a-z]', password):
        raise ValidatePasswordException("The password must contain at least one lowercase letter.")
