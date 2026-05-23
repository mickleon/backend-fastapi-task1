import logging

from application.core.exceptions.database_exceptions import (
    ImageNotFoundException,
    PostNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    ImageNotFoundByIdException,
    PostNotFoundByIdException,
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


class CreateCommentAdminUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(
        self,
        data: CommentRequestSchema,
        current_user: UserResponseSchema,
    ) -> CommentResponseSchema:
        async with self._database.session() as session:
            try:
                comment = await self._repo.create(
                    session=session, data=data, author_id=current_user.id
                )
            except PostNotFoundException:
                error = PostNotFoundByIdException(id=data.post_id)
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

            return CommentResponseSchema.model_validate(obj=comment)
