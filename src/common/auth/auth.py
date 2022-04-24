from typing import Literal, Optional
from fastapi import Security
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.api_key import APIKeyBase
from starlette.requests import Request

UserRole = Literal["ADMIN", "USER"]

# FIXME: if create 2 APIKeyHeader only last one will work


class UserIdSchema(APIKeyBase):
    def __init__(self) -> None:
        super().__init__()

        self.model = APIKey(**{"in": APIKeyIn.header}, name="X-User-Id")

        self.scheme_name = self.__class__.__name__

    def __call__(self, request: Request) -> Optional[int]:
        header = request.headers.get(self.model.name)
        if not header:
            return None

        id = int(header)
        return id if id else None


class UserRoleSchema(APIKeyBase):
    def __init__(self) -> None:
        super().__init__()

        self.model = APIKey(**{"in": APIKeyIn.header}, name="X-User-Role")

        self.scheme_name = self.__class__.__name__

    def __call__(self, request: Request) -> UserRole:
        header = request.headers.get(self.model.name)
        if not header:
            return "USER"

        try:
            return UserRole(header)
        except ValueError:
            return "USER"


user_id_schema = UserIdSchema()
user_role_schema = UserRoleSchema()


def get_user_id(user_str: Optional[str] = Security(user_id_schema)) -> Optional[int]:
    user_id = int(user_str, base=10)
    return user_id if user_id != 0 else None


def get_user_role(role: Optional[UserRole] = Security(user_role_schema)) -> UserRole:
    return role if role else "USER"
