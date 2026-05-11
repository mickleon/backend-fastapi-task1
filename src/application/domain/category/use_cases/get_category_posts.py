import logging
import uuid

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.category import (
    CategoryRepository,
)
from application.schemas.post import (
    PostResponseSchema,
    PostsPageResponseSchema,
)
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class GetCategoryPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self,
        id: uuid.UUID,
        page: int,
        page_size: int,
        current_user: UserResponseSchema | None,
    ) -> PostsPageResponseSchema:
        page = max(page, 1)
        limit = max(min(page_size, 100), 1)
        offset = (page - 1) * limit

        async with self._database.session() as session:
            try:
                posts = await self._repo.get_posts_published(
                    session=session,
                    id=id,
                    offset=offset,
                    limit=limit + 1,
                )
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=id)
                username = (
                    current_user.username
                    if current_user is not None
                    else 'анонимный'
                )
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error

            has_next = len(posts) > limit
            if has_next:
                posts = posts[:limit]

            posts_data = [
                PostResponseSchema.model_validate(obj=post) for post in posts
            ]

            return PostsPageResponseSchema(
                items=posts_data,
                has_next=has_next,
            )
