from auth_manager import AuthManager
from jwt_utils import JWTUtil
from repository import UserRepository, PostgresqlUserRepository

from os import getenv
from fastapi import Depends

PRIVATE_KEY_PATH = getenv("PRIVATE_KEY_PATH")
PUBLIC_KEY_PATH = getenv("PUBLIC_KEY_PATH")

db_variables = {
    "POSTGRES_USER": getenv("POSTGRES_USER"),
    "POSTGRES_PASSWORD": getenv("POSTGRES_PASSWORD"),
    "POSTGRES_DB": getenv("POSTGRES_DB"),
    "POSTGRES_HOST": getenv("POSTGRES_HOST"),
    "POSTGRES_PORT": getenv("POSTGRES_PORT"),
}

for var, value in db_variables.items():
    if value is None:
        print(f"WARNING: Missing environment variable: {var}")

# Singleton
database: UserRepository = PostgresqlUserRepository(
    database_name=db_variables["POSTGRES_DB"],
    database_user=db_variables["POSTGRES_USER"],
    database_password=db_variables["POSTGRES_PASSWORD"],
    host_database=db_variables["POSTGRES_HOST"],
    port_database=db_variables["POSTGRES_PORT"]
)

def get_user_repository() -> UserRepository:
    return database

def get_auth_manager(repository: UserRepository = Depends(get_user_repository)) -> AuthManager:
    return AuthManager(repository)

def get_jwt_util() -> JWTUtil:
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return JWTUtil(f.read(), "RS256")

def get_public_key() -> str:
    with open(PUBLIC_KEY_PATH, "rb") as f:
        return f.read()
