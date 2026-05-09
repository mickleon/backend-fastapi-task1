import logging
import uuid

from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.post import (
    PostRepository,
)
from application.schemas.comment import (
    CommentResponseSchema,
    CommentsPageResponseSchema,
)
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class GetPostCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self,
        id: uuid.UUID,
        page: int,
        page_size: int,
        current_user: UserResponseSchema | None,
    ) -> CommentsPageResponseSchema:
        page = max(page, 1)
        limit = max(min(page_size, 100), 1)
        offset = (page - 1) * limit

        async with self._database.session() as session:
            try:
                comments = await self._repo.get_comments(
                    session=session,
                    id=id,
                    offset=offset,
                    limit=limit + 1,
                )
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=id)
                username = (
                    current_user.username
                    if current_user is not None
                    else 'анонимный'
                )
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error

            has_next = len(comments) > limit
            if has_next:
                comments = comments[:limit]

            comments_data = [
                CommentResponseSchema.model_validate(obj=comment)
                for comment in comments
            ]

            return CommentsPageResponseSchema(
                items=comments_data,
                has_next=has_next,
            )
