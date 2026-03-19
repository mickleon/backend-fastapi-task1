from src.core.exceptions.database_exceptions import (
    UserUsernameAlreadyExistsException,
    UserEmailAlreadyExistsException,
)
from src.core.exceptions.domain_exceptions import (
    UserUsernameIsNotUniqueException,
    UserEmailIsNotUniqueException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.user import UserRequestSchema, UserResponseSchema


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserRequestSchema):
        with self._database.session() as session:
            try:
                user = self._repo.create(session=session, data=data)
            except UserUsernameAlreadyExistsException:
                raise UserUsernameIsNotUniqueException(username=data.username)
            except UserEmailAlreadyExistsException:
                raise UserEmailIsNotUniqueException(email=data.email)

            return UserResponseSchema.model_validate(obj=user)
