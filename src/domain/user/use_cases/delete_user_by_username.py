from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByUsernameException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository


class DeleteUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str) -> None:
        with self._database.session() as session:
            try:
                self._repo.delete(session=session, username=username)
            except UserNotFoundException:
                raise UserNotFoundByUsernameException(username=username)
