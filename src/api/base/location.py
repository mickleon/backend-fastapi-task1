import uuid
from fastapi import APIRouter, status

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
    return await use_case.execute(id=id)


@location_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_location(data: LocationRequestSchema) -> LocationResponseSchema:
    use_case = CreateLocationUseCase()
    return await use_case.execute(data=data)


@location_router.put('/{id}')
async def update_location(
    id: uuid.UUID, data: LocationRequestSchema
) -> LocationResponseSchema:
    use_case = UpdateLocationUseCase()
    return await use_case.execute(id=id, data=data)


@location_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(id: uuid.UUID):
    use_case = DeleteLocationUseCase()
    await use_case.execute(id)
    return {'message': f'Местоположение с id "{id}" успешно удалено'}

