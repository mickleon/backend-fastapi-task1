import uuid
from fastapi import APIRouter, HTTPException, status

from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from src.domain.location.use_cases.create_location import CreateLocationUseCase
from src.domain.location.use_cases.delete_location import (
    DeleteLocationUseCase,
)
from src.domain.location.use_cases.get_location import (
    GetLocationUseCase,
)
from src.domain.location.use_cases.update_location import (
    UpdateLocationUseCase,
)
from src.schemas.location import LocationResponseSchema, LocationRequestSchema

location_router = APIRouter()


@location_router.get('/{id}')
async def get_location(id: uuid.UUID) -> LocationResponseSchema:
    use_case = GetLocationUseCase()
    try:
        location = await use_case.execute(id=id)
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    return location


@location_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_location(
    data: LocationRequestSchema,
) -> LocationResponseSchema:
    use_case = CreateLocationUseCase()
    location = await use_case.execute(data=data)
    return location


@location_router.put('/{id}')
async def update_location(
    id: uuid.UUID, data: LocationRequestSchema
) -> LocationResponseSchema:
    use_case = UpdateLocationUseCase()
    try:
        location = await use_case.execute(id=id, data=data)
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    return location


@location_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(id: uuid.UUID):
    use_case = DeleteLocationUseCase()
    try:
        await use_case.execute(id)
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
