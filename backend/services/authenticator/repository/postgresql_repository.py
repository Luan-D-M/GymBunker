from repository.user import User
from repository import UserRepository

import psycopg
import contextlib

class PostgresqlUserRepository(UserRepository):
    """
    A repository class for managing User data in a PostgreSQL database.

    This class implements the UserRepository interface for PostgreSQL, handling
    database connections, and CRUD-like operations for users.
    """


    def __init__(self, database_name, database_user, database_password, host_database, port_database):
        self.__conn_details = {
            "dbname": database_name,
            "user": database_user,
            "password": database_password,
            "host": host_database,
            "port": port_database
        }

    @contextlib.asynccontextmanager     # So it is possible to call in a 'with' statement.
    async def __connect(self):
        """
        A private context manager to establish and manage a database connection.
        """

        # https://www.psycopg.org/psycopg3/docs/advanced/async.html
        # AsyncConnectionPool would have better performance
        async with await psycopg.AsyncConnection.connect(**self.__conn_details, autocommit=True) as conn:
            async with conn.cursor() as cur:
              yield cur
        

    async def get(self, username: str) -> User | None:
        """
        Retrieves a user from the database by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: The User object if found, otherwise returns None. 
        """

        async with self.__connect() as cursor:
            await cursor.execute(
                "SELECT username, password_hash, id FROM users WHERE username = %s",
                (username,)
            )
            row = await cursor.fetchone()
            if row:
                return User(username=row[0], password_hash=row[1], id=row[2])
            return None


    async def get_all(self) -> list[User]:
        """
        Retrieves all users from the database.

        Returns:
            List[User]: A list of User objects. Returns an empty list if no users are found.
        """

        sql_query = "SELECT username, password_hash, id FROM users"
        users_list: list[User] = [] 
        async with self.__connect() as cursor:
            await cursor.execute(sql_query)
            rows = await cursor.fetchall()
            for row in rows:
                users_list.append(User(username=row[0], password_hash=row[1], id=row[2]))
        return users_list


    async def add_user(self, username: str, password_hash: str) -> None:
        """
        Adds a new user with their username and password hash to the database.
        """
        async with self.__connect() as cursor:
            await cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash)
            )


    async def update_hash(self, username: str, new_password_hash: str) -> None:
        """
        Updates the password hash for an existing user identified by their username.
        """
        async with self.__connect() as cursor:
              await cursor.execute(
                   "UPDATE users SET password_hash=%s WHERE username=%s",
                   (new_password_hash, username)
              )


    async def delete(self, username: str) -> None:
        """
        Deletes a user from the database based on their username.
        """
        async with self.__connect() as cursor:
            await cursor.execute(
                "DELETE FROM users WHERE username = %s",
                (username,)
            )


    async def check_if_username_already_exists(self, username: str) -> bool:
        """
        Checks if a username already exists in the users table.
        """
        async with self.__connect() as cursor:
            await cursor.execute(
                "SELECT 1 FROM users WHERE username = %s",
                (username,)
            )
            result = await cursor.fetchone()

            return result is not None