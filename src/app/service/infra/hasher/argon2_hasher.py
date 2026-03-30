from argon2 import PasswordHasher, exceptions

from src.app.service.infra.hasher.password_hasher import BasePasswordHasher


class Argon2PasswordHasher(BasePasswordHasher):
    def __init__(self):
        self. hasher = PasswordHasher()

    def hash(self, password) -> str:
        return self.hasher.hash(password)
    
    def verify(self, hashed_password, plain_password) -> bool:
        """パスワードがマッチしない場合はFalseを返す"""
        try:
            return self.hasher.verify(hashed_password, plain_password)
        except exceptions.VerifyMismatchError:
            return False