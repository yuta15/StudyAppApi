from uuid import UUID
from abc import ABC, abstractmethod

from src.app.model.user.principals.user import User


class UserRepository(ABC):
    @abstractmethod
    def create_user(user:User) -> User:...

    @abstractmethod
    def get_user(user_id:UUID) -> User:...

    @abstractmethod
    def update_user(user:User) -> User:...

    @abstractmethod
    def delete_user(user:User) -> None:...
