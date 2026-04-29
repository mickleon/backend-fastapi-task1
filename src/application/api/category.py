import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from application.api.depends import (
    create_category_use_case,
    delete_category_use_case,
    get_category_use_case,
    update_category_use_case,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
)
from application.domain.category.use_cases.create_category import (
    CreateCategoryUseCase,
)
from application.domain.category.use_cases.delete_category import (
    DeleteCategoryUseCase,
)
from application.domain.category.use_cases.get_category import (
    GetCategoryUseCase,
)
from application.domain.category.use_cases.update_category import (
    UpdateCategoryUseCase,
)
from application.schemas.category import (
    CategoryResponseSchema,
    CategoryRequestSchema,
)
from application.schemas.user import UserResponseSchema
from application.services.auth import AuthService

router = APIRouter()


@router.get('/{id}', response_model=CategoryResponseSchema)
async def get_category(
    id: uuid.UUID,
    use_case: GetCategoryUseCase = Depends(get_category_use_case),
    current_user: UserResponseSchema | None = Depends(
        AuthService.get_current_user_or_none
    ),
) -> CategoryResponseSchema:
    try:
        return await use_case.execute(id=id, current_user=current_user)
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
    current_user: UserResponseSchema = Depends(AuthService.get_current_user),
) -> CategoryResponseSchema:
    return await use_case.execute(data=data, current_user=current_user)


@router.put(
    '/{id}',
    response_model=CategoryResponseSchema,
)
async def update_category(
    id: uuid.UUID,
    data: CategoryRequestSchema,
    use_case: UpdateCategoryUseCase = Depends(update_category_use_case),
    current_user: UserResponseSchema = Depends(AuthService.get_current_user),
) -> CategoryResponseSchema:
    try:
        return await use_case.execute(
            id=id, data=data, current_user=current_user
        )
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    id: uuid.UUID,
    use_case: DeleteCategoryUseCase = Depends(delete_category_use_case),
    current_user: UserResponseSchema = Depends(AuthService.get_current_user),
):
    try:
        await use_case.execute(id, current_user=current_user)
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
