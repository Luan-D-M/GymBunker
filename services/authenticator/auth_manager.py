from repository import UserRepository
from repository.user import User

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class AuthManager: 

    def __init__(self, user_repository: UserRepository) -> None:
        self.__user_repository = user_repository
        self.__hasher = PasswordHasher()


    async def username_exists(self, username: str) -> bool:
        """
            Check if username already exists.
        """

        return await self.__user_repository.check_if_username_already_exists(username)
    
    # Maybe rename that function --> it is not precise --> why not "create_user" and some documentation?
    async def hash_password_and_store_user_in_database(self, username: str, password: str) -> None:
        hashed_password = self.__hash_password(password)
        await self.__user_repository.add_user(username, hashed_password)


    async def verify_password_and_update_its_hash_in_database_if_needed(self, username: str, password: str) -> bool:
        """
        Verify user's password and update its hash stored in database if there are
        new parameters available (argon2 library handles that).

        Returns False if password is incorrect or if username doesn't exists.
        """

        user: User = await self.__user_repository.get(username)
        if user is None:
            return False

        try:    
            self.__hasher.verify(user.password_hash, password)

            password_needs_to_be_updated = self.__hasher.check_needs_rehash(user.password_hash)
            if password_needs_to_be_updated:
                # Re-hash and update the database
                new_hash = self.__hasher.hash(password)
                await self.__user_repository.update_hash(username, new_hash)
            return True
        except VerifyMismatchError:
            return False

    async def delete_user(self, username: str):
        await self.__user_repository.delete(username)

    def __hash_password(self, password: str) -> str:
        """
            Hash user's password
        """

        return self.__hasher.hash(password)