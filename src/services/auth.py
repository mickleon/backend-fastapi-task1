from typing import Annotated
from fastapi import Depends
from pydantic import SecretStr
from jose import JWTError, jwt

from src.core.exceptions.auth_exceptions import CredentialsException
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.schemas.user import UserResponseSchema
from src.resources.auth import oauth2_scheme
from src.infrastructure.sqlite.database import (
    database as sqlite_database,
    Database,
)
from src.infrastructure.sqlite.repositories.user import UserRepository

AUTH_EXCEPTION_MESSAGE = 'Невозможно проверить данные авторизации'
SECRET_AUTH_KEY = SecretStr(
    'qqZmvlTRAksPycvJ3e6Eolah99O8O35F3JpUPMyd8Tnewqjolsnw6HWi1VD'
)
AUTH_ALGORITHM = 'HS256'


class AuthService:
    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UserResponseSchema:
        _database: Database = sqlite_database
        _repo: UserRepository = UserRepository()

        try:
            payload = jwt.decode(
                token=token,
                key=SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[AUTH_ALGORITHM],
            )
            username = payload.get('sub')
            if username is None:
                raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
        except JWTError:
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

        try:
            with _database.session() as session:
                user = _repo.get(session=session, username=username)
        except UserNotFoundException:
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

        return UserResponseSchema.model_validate(obj=user)
