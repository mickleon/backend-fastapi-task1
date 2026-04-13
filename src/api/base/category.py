import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import (
    create_category_use_case,
    delete_category_use_case,
    get_category_use_case,
    update_category_use_case,
)
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
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

router = APIRouter()


@router.get('/{id}', response_model=CategoryResponseSchema)
async def get_category(
    id: uuid.UUID,
    use_case: GetCategoryUseCase = Depends(get_category_use_case),
) -> CategoryResponseSchema:
    try:
        return await use_case.execute(id=id)
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponseSchema,
)
async def create_category(
    data: CategoryRequestSchema,
    use_case: CreateCategoryUseCase = Depends(create_category_use_case),
) -> CategoryResponseSchema:
    return await use_case.execute(data=data)


@router.put('/{id}', response_model=CategoryResponseSchema)
async def update_category(
    id: uuid.UUID,
    data: CategoryRequestSchema,
    use_case: UpdateCategoryUseCase = Depends(update_category_use_case),
) -> CategoryResponseSchema:
    try:
        return await use_case.execute(id=id, data=data)
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    id: uuid.UUID,
    use_case: DeleteCategoryUseCase = Depends(delete_category_use_case),
):
    try:
        await use_case.execute(id)
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
