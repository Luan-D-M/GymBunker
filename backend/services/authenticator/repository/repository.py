from abc import ABC, abstractmethod
from repository.user import User

class UserRepository(ABC):
    @abstractmethod
    async def get(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def add_user(self, username: str, password_hash: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_hash(self, username: str, new_password_hash: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, username: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def check_if_username_already_exists(self, username: str) -> bool:
        raise NotImplementedError
