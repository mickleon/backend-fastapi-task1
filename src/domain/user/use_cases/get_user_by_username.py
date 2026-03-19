from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByUsernameException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.user import UserResponseSchema


class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str) -> UserResponseSchema:
        with self._database.session() as session:
            try:
                user = self._repo.get(session=session, username=username)
            except UserNotFoundException:
                raise UserNotFoundByUsernameException(username=username)

            return UserResponseSchema.model_validate(obj=user)
