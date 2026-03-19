from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository


class DeleteUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str):
        with self._database.session() as session:
            self._repo.delete(session=session, username=username)
