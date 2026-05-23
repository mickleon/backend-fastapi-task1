import logging

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    ImageNotFoundException,
    LocationNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    ImageNotFoundByIdException,
    LocationNotFoundByIdException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.post import (
    PostRepository,
)
from application.schemas.post import (
    PostRequestAdminSchema,
    PostResponseSchema,
)
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class CreatePostAdminUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self,
        data: PostRequestAdminSchema,
        current_user: UserResponseSchema,
    ) -> PostResponseSchema:
        async with self._database.session() as session:
            try:
                post = await self._repo.create(
                    session=session, data=data, author_id=current_user.id
                )
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
            except ImageNotFoundException as exception:
                error = ImageNotFoundByIdException(id=exception.id)
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error

            return PostResponseSchema.model_validate(obj=post)
