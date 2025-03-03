import bcrypt

from cryptoapp.domain.entities.user.hasher import PasswordHasher


class Hasher(PasswordHasher):
    def hash(self, password: str) -> str:
        hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed_bytes.decode("utf-8")

    def verify(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
