import logging

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
from application.schemas.comment import CommentResponseSchema
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class GetCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self,
        id: int,
        current_user: UserResponseSchema | None,
    ) -> CommentResponseSchema:
        async with self._database.session() as session:
            try:
                comment = await self._repo.get(session=session, id=id)
            except CommentNotFoundException:
                error = CommentNotFoundByIdException(id=id)
                username = (
                    current_user.username
                    if current_user is not None
                    else 'анонимный'
                )
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error

            return CommentResponseSchema.model_validate(obj=comment)
