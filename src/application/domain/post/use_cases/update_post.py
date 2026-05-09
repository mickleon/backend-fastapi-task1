import logging
import uuid

from application.core.exceptions.auth_exceptions import AccessDeniedException
from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.post import (
    PostRepository,
)
from application.schemas.post import PostRequestSchema, PostResponseSchema
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self,
        id: uuid.UUID,
        data: PostRequestSchema,
        current_user: UserResponseSchema,
    ) -> PostResponseSchema:
        async with self._database.session() as session:
            try:
                post = await self._repo.get(session=session, id=id)
                if post.author_id == current_user.id or current_user.is_admin:
                    post = await self._repo.update(
                        session=session,
                        id=id,
                        data=data,
                    )
                else:
                    error = AccessDeniedException()
                    logger.error(
                        f'Доступ запрещен: пользователь {current_user.username} попытался отредактировать публикацию с id {post.id}'
                    )
                    raise error
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
