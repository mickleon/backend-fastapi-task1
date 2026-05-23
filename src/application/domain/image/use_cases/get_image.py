import logging
import uuid

from fastapi.responses import FileResponse

from application.core.exceptions.database_exceptions import (
    ImageNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    ImageNotFoundByIdException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.image import (
    ImageRepository,
)

logger = logging.getLogger(__name__)


class GetImageUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = ImageRepository()
        self.image_folder = '/images'

    async def execute(self, id: uuid.UUID) -> FileResponse:
        try:
            async with self._database.session() as session:
                image = await self._repo.get(session=session, id=id)
        except ImageNotFoundException:
            error = ImageNotFoundByIdException(id=id)
            logger.error(f'Изображение не найдено: {error.get_detail()}')
            raise error

        full_image_path: str = f'{self.image_folder}/{image.path}.jpg'
        return FileResponse(full_image_path, media_type='image/jpeg')
