import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import (
    create_location_use_case,
    delete_location_use_case,
    get_location_use_case,
    update_location_use_case,
)
from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from src.domain.location.use_cases.create_location import CreateLocationUseCase
from src.domain.location.use_cases.delete_location import DeleteLocationUseCase
from src.domain.location.use_cases.get_location import GetLocationUseCase
from src.domain.location.use_cases.update_location import UpdateLocationUseCase
from src.schemas.location import LocationResponseSchema, LocationRequestSchema
from src.schemas.user import UserResponseSchema
from src.services.auth import AuthService

router = APIRouter()


@router.get('/{id}', response_model=LocationResponseSchema)
async def get_location(
    id: uuid.UUID,
    use_case: GetLocationUseCase = Depends(get_location_use_case),
    current_user: UserResponseSchema | None = Depends(
        AuthService.get_current_user_or_none
    ),
) -> LocationResponseSchema:
    try:
        return await use_case.execute(id=id, current_user=current_user)
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=LocationResponseSchema,
)
async def create_location(
    data: LocationRequestSchema,
    use_case: CreateLocationUseCase = Depends(create_location_use_case),
    current_user: UserResponseSchema = Depends(AuthService.get_current_user),
) -> LocationResponseSchema:
    return await use_case.execute(data=data, current_user=current_user)


@router.put(
    '/{id}',
    response_model=LocationResponseSchema,
)
async def update_location(
    id: uuid.UUID,
    data: LocationRequestSchema,
    use_case: UpdateLocationUseCase = Depends(update_location_use_case),
    current_user: UserResponseSchema = Depends(AuthService.get_current_user),
) -> LocationResponseSchema:
    try:
        return await use_case.execute(
            id=id, data=data, current_user=current_user
        )
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_location(
    id: uuid.UUID,
    use_case: DeleteLocationUseCase = Depends(delete_location_use_case),
    current_user: UserResponseSchema = Depends(AuthService.get_current_user),
):
    try:
        await use_case.execute(id, current_user=current_user)
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
