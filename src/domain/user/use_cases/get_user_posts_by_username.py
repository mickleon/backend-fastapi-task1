import logging

from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByUsernameException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.post import PostResponseSchema, PostsPageResponseSchema
from src.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class GetUserPostsByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        target_username: str,
        page: int,
        page_size: int,
        current_user: UserResponseSchema | None,
    ) -> PostsPageResponseSchema:
        page = max(page, 1)
        limit = max(min(page_size, 100), 1)
        offset = (page - 1) * limit

        with self._database.session() as session:
            try:
                posts = self._repo.get_posts(
                    session=session,
                    username=target_username,
                    offset=offset,
                    limit=limit + 1,
                )
            except UserNotFoundException:
                error = UserNotFoundByUsernameException(
                    username=target_username
                )
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
