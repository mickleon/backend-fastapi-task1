import logging

from application.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.comment import (
    CommentRepository,
)
from application.schemas.comment import (
    CommentRequestSchema,
    CommentResponseSchema,
)
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self,
        id: int,
        data: CommentRequestSchema,
        current_user: UserResponseSchema,
    ) -> CommentResponseSchema:
        async with self._database.session() as session:
            try:
                comment = await self._repo.update(
                    session=session, id=id, data=data
                )
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=id)
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=data.post_id)
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error
            except UserNotFoundException:
                error = UserNotFoundByIdException(id=data.author_id)
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error

            return CommentResponseSchema.model_validate(obj=comment)
