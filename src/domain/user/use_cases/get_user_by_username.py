from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.user import UserResponseSchema


class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str) -> UserResponseSchema:
        with self._database.session() as session:
            user = self._repo.get(session=session, username=username)

            return UserResponseSchema.model_validate(obj=user)
