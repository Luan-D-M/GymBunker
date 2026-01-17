from repository.user import User
from repository import UserRepository

class MockRepository(UserRepository):
    """
    A repository class for testing that simulates a database using an in-memory dictionary.
    """

    def __init__(self):
        """Initializes the mock database as an empty dictionary."""
        self.__mockDb = {}

    async def get(self, username: str) -> User | None:
        """
        Retrieves a user from the mock database by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: The User object if found, otherwise returns None.
        """
        
        # The .get() method of a dictionary returns None if the key doesn't exist.
        return self.__mockDb.get(username)

    async def get_all(self) -> list[User]:
        """
        Retrieves all users from the mock database.

        Returns:
            List[User]: A list of all User objects.
        """

        return list(self.__mockDb.values())


    async def add_user(self, username: str, password_hash: str) -> None:
        """
        Adds a new user with their username and password hash to the mock database.
        """
        if username not in self.__mockDb:     # Postgresql repository doesnt check that
            new_user = User(username=username, password_hash=password_hash)
            self.__mockDb[username] = new_user


    async def update_hash(self, username: str, new_password_hash: str) -> None:
        """
        Updates the password hash for an existing user in the mock database.
        """
        if username in self.__mockDb:
            self.__mockDb[username].password_hash = new_password_hash


    async def delete(self, username: str) -> None:
        """
        Deletes a user from the mock database based on their username.
        """
        if username in self.__mockDb:
            del self.__mockDb[username]


    async def check_if_username_already_exists(self, username: str) -> bool:
        """
        Checks if a username already exists in the mock database.
        """

        return username in self.__mockDb
    
    def clear(self):
        self.__mockDb = {}