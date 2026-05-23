import io
import logging
import uuid
from pathlib import Path

from fastapi import UploadFile
from PIL import Image

from application.core.exceptions.domain_exceptions import (
    UploadFileIsNotImageException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.image import (
    ImageRepository,
)
from application.schemas.image import ImageUploadResponseSchema
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class UploadImagesUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = ImageRepository()
        self.image_folder = '/images'
        self.max_size = (1920, 1920)
        self.quality = 85

    async def execute(
        self, images: list[UploadFile], current_user: UserResponseSchema
    ) -> list[ImageUploadResponseSchema]:
        saved_ids: list[uuid.UUID] = []

        Path(self.image_folder).mkdir(parents=True, exist_ok=True)

        for image in images:
            contents = await image.read()

            try:
                pil_image = Image.open(io.BytesIO(contents))
            except Exception:
                error = UploadFileIsNotImageException()
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error

            pil_image.thumbnail(self.max_size, Image.Resampling.LANCZOS)

            image_id = uuid.uuid4()
            new_image_path = f'{self.image_folder}/{image_id}.jpg'

            pil_image.save(
                new_image_path,
                'JPEG',
                quality=self.quality,
                optimize=True,
                progressive=True,
            )

            saved_ids.append(image_id)

        async with self._database.session() as session:
            images_created = await self._repo.bulk_create(
                session=session, ids=saved_ids
            )

        return [
            ImageUploadResponseSchema(id=img.id) for img in images_created
        ]
