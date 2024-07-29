from typing import Dict

from cryptoapp.application.interfaces.identifier import IUserIdentifier


class UserIdentifier(IUserIdentifier):
    def get_user_id(self, data: Dict[str, str | int]) -> int:
        return data["sub"]  # type: ignore
