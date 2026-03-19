import uuid
from fastapi import APIRouter, status

from src.domain.category.use_cases.create_category import CreateCategoryUseCase
from src.domain.category.use_cases.delete_category import (
    DeleteCategoryUseCase,
)
from src.domain.category.use_cases.get_category import (
    GetCategoryUseCase,
)
from src.domain.category.use_cases.update_category import (
    UpdateCategoryUseCase,
)
from src.schemas.category import CategoryResponseSchema, CategoryRequestSchema

category_router = APIRouter()


@category_router.get('/{id}')
async def get_category(id: uuid.UUID) -> CategoryResponseSchema:
    use_case = GetCategoryUseCase()
    return await use_case.execute(id=id)


@category_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryRequestSchema,
) -> CategoryResponseSchema:
    use_case = CreateCategoryUseCase()
    return await use_case.execute(data=data)


@category_router.put('/{id}')
async def update_category(
    id: uuid.UUID, data: CategoryRequestSchema
) -> CategoryResponseSchema:
    use_case = UpdateCategoryUseCase()
    return await use_case.execute(id=id, data=data)


@category_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id: uuid.UUID):
    use_case = DeleteCategoryUseCase()
    await use_case.execute(id)
    return {'message': f'Категория с id "{id}" успешно удаленa'}
