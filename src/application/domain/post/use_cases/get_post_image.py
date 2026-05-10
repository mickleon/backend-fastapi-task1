import logging
import uuid

from fastapi.responses import FileResponse

from application.core.exceptions.database_exceptions import (
    PostNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    PostHasNoImageException,
    PostNotFoundByIdException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.post import (
    PostRepository,
)
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class GetPostImageUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = PostRepository()
        self.image_folder = '/images'

    async def execute(
        self, post_id: uuid.UUID, current_user: UserResponseSchema | None
    ) -> FileResponse:
        try:
            async with self._database.session() as session:
                post = await self._repo.get(session=session, id=post_id)
        except PostNotFoundException:
            error = PostNotFoundByIdException(id=post_id)

            username = (
                current_user.username
                if current_user is not None
                else 'анонимный'
            )
            logger.error(
                f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
            )
            raise error
        if not post.image_path:
            error = PostHasNoImageException(id=post_id)

            username = (
                current_user.username
                if current_user is not None
                else 'анонимный'
            )
            logger.error(
                f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
            )
            raise error

        full_image_path: str = f'{self.image_folder}/{post.image_path}.jpg'
        return FileResponse(full_image_path, media_type='image/jpeg')
