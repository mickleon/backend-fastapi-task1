import io
import logging
import uuid
from pathlib import Path

from fastapi import UploadFile
from PIL import Image

from application.core.exceptions.domain_exceptions import (
    UploadFileIsNotImageException,
)
from application.schemas.post import PostImageResponse
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class AddPostImageUseCase:
    def __init__(self) -> None:
        self.image_folder = '/images'
        self.max_size = (1920, 1920)
        self.quality = 85

    async def execute(
        self, image: UploadFile, current_user: UserResponseSchema
    ) -> PostImageResponse:
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

        new_image_name = str(uuid.uuid4())
        new_image_path = f'{self.image_folder}/{new_image_name}.jpg'

        Path(self.image_folder).mkdir(parents=True, exist_ok=True)

        pil_image.save(
            new_image_path,
            'JPEG',
            quality=self.quality,
            optimize=True,
            progressive=True,
        )

        return PostImageResponse(image_path=new_image_name)
