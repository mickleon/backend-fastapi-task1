from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.user import User
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.user import UserRequestSchema, UserResponseSchema


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserRequestSchema):
        with self._database.session() as session:
            user = User(
                **data.model_dump(exclude={'password'}),
                password=data.password.get_secret_value(),
            )
            self._repo.create(session=session, user=user)

        return UserResponseSchema.model_validate(obj=user)

