from src.core.exceptions.database_exceptions import (
    UserEmailAlreadyExistsException,
    UserNotFoundException,
    UserUsernameAlreadyExistsException,
)
from src.core.exceptions.domain_exceptions import (
    UserEmailIsNotUniqueException,
    UserNotFoundByUsernameException,
    UserUsernameIsNotUniqueException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.user import UserRequestSchema, UserResponseSchema


class UpdateUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self, username: str, data: UserRequestSchema
    ) -> UserResponseSchema:
        with self._database.session() as session:
            try:
                user = self._repo.update(
                    session=session, username=username, data=data
                )
            except UserNotFoundException:
                raise UserNotFoundByUsernameException(username=username)
            except UserUsernameAlreadyExistsException:
                raise UserUsernameIsNotUniqueException(username=data.username)
            except UserEmailAlreadyExistsException:
                raise UserEmailIsNotUniqueException(email=data.email)

            return UserResponseSchema.model_validate(obj=user)
