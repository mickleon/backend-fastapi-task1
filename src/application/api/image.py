from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from starlette.responses import FileResponse

from application.api.depends import get_image_use_case, upload_images_use_case
from application.core.exceptions.domain_exceptions import (
    ImageNotFoundByIdException,
    UploadFileIsNotImageException,
)
from application.domain.image.use_cases.get_image import GetImageUseCase
from application.domain.image.use_cases.upload_images import (
    UploadImagesUseCase,
)
from application.schemas.image import ImageUploadResponseSchema
from application.schemas.user import UserResponseSchema
from application.services.auth import AuthService

router = APIRouter()


@router.post(
    '/upload',
    status_code=status.HTTP_201_CREATED,
    response_model=list[ImageUploadResponseSchema],
    openapi_extra={
        'requestBody': {
            'content': {
                'multipart/form-data': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'images': {
                                'type': 'array',
                                'items': {'type': 'string', 'format': 'binary'},
                            }
                        },
                        'required': ['images'],
                    }
                }
            }
        }
    },
)
async def upload_images(
    images: list[UploadFile] = File(),
    use_case: UploadImagesUseCase = Depends(upload_images_use_case),
    current_user: UserResponseSchema = Depends(AuthService.get_current_user),
) -> list[ImageUploadResponseSchema]:
    try:
        return await use_case.execute(images=images, current_user=current_user)
    except UploadFileIsNotImageException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.get_detail()
        )


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
)
async def get_image(
    id: uuid.UUID,
    use_case: GetImageUseCase = Depends(get_image_use_case),
) -> FileResponse:
    try:
        return await use_case.execute(id=id)
    except ImageNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
