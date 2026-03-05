from fastapi import HTTPException

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository


class DeleteUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str):
        with self._database.session() as session:
            user = self._repo.get(session=session, username=username)

            if user is None:
                raise HTTPException(
                    status_code=404, detail=f'Пользователь "{username}" не найден'
                )

        self._repo.delete(session=session, user=user)
