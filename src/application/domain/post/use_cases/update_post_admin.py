import logging
import uuid

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    PostNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    PostNotFoundByIdException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.post import (
    PostRepository,
)
from application.schemas.post import (
    PostResponseSchema,
    PostUpdateAdminSchema,
)
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class UpdatePostAdminUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self,
        id: uuid.UUID,
        data: PostUpdateAdminSchema,
        current_user: UserResponseSchema,
    ) -> PostResponseSchema:
        async with self._database.session() as session:
            try:
                post = await self._repo.update(
                    session=session,
                    id=id,
                    data=data,
                )
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=id)
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
