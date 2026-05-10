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
from application.infrastructure.postgress.repositories.user import (
    UserRepository,
)
from application.schemas.post import PostResponseSchema
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class GetPostAdminUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()

    async def execute(
        self,
        id: uuid.UUID,
        current_user: UserResponseSchema | None,
    ) -> PostResponseSchema:
        async with self._database.session() as session:
            try:
                post = await self._repo.get(session=session, id=id)
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

            return PostResponseSchema.model_validate(obj=post)
