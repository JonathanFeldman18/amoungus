from src.my_exceptions.checking_deployment_exception import CheckingDeploymentException

def validate_if_contains_space(db_name: str, username: str) -> bool:
    if ' ' in db_name:
        raise CheckingDeploymentException("The db_name should not contain spaces.")
    elif ' ' in username:
        raise CheckingDeploymentException("The username should not contain spaces.")
    return True

def validate_db_name(db_name: str) -> bool:
    if not db_name.startswith("matmon25-"):
        raise CheckingDeploymentException("Database must start with 'matmon25-'")
    return True

def validate_username(username: str) -> bool:
    if not len(username) >= 3:
        raise CheckingDeploymentException("Username must be at least 3 characters.")
    return True

def validate_deployment(db_name: str, username: str) -> bool:
    validate_if_contains_space(db_name, username)
    validate_db_name(db_name)
    validate_username(username)
    return True