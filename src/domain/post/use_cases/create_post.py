import logging

from src.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    UserNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    UserNotFoundByIdException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.post import PostRequestSchema, PostResponseSchema
from src.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self,
        data: PostRequestSchema,
        current_user: UserResponseSchema,
    ) -> PostResponseSchema:
        with self._database.session() as session:
            try:
                post = self._repo.create(session=session, data=data)
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=data.author_id)
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=data.category_id)  # pyright: ignore[reportArgumentType]
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error
            except LocationNotFoundException:
                error = LocationNotFoundByIdException(id=data.location_id)  # pyright: ignore[reportArgumentType]
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error

            return PostResponseSchema.model_validate(obj=post)
