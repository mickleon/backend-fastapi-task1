import logging

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
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, id: int, current_user: UserResponseSchema) -> None:
        if not current_user.is_admin:
            error = AccessDeniedException()
            logger.error(
                f'Доступ запрещен: пользователь {current_user.username} попытался удалить комментарий с id {id}'
            )
            raise error
        async with self._database.session() as session:
            try:
                await self._repo.delete(session=session, id=id)
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=id)
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error
