import logging
import uuid

from application.core.exceptions.auth_exceptions import AccessDeniedException
from application.core.exceptions.database_exceptions import (
    CommentNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.comment import (
    CommentRepository,
)
from application.schemas.comment import (
    CommentResponseSchema,
    CommentUpdateSchema,
)
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self,
        id: uuid.UUID,
        data: CommentUpdateSchema,
        current_user: UserResponseSchema,
    ) -> CommentResponseSchema:
        async with self._database.session() as session:
            try:
                comment = await self._repo.get_published(session=session, id=id)
                if comment.author_id == current_user.id:
                    comment = await self._repo.update(
                        session=session, id=id, data=data
                    )
                else:
                    error = AccessDeniedException()
                    logger.error(
                        f'Доступ запрещен: пользователь {current_user.username} попытался отредактировать комментарий с id {comment.id}'
                    )
                    raise error
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=id)
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error

            return CommentResponseSchema.model_validate(obj=comment)
