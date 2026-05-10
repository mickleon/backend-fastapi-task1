import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status

from application.api.depends import (
    get_category_posts_use_case,
    get_category_use_case,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
)
from application.domain.category.use_cases.get_category import (
    GetCategoryUseCase,
)
from application.domain.category.use_cases.get_category_posts import (
    GetCategoryPostsUseCase,
)
from application.schemas.category import (
    CategoryResponseSchema,
)
from application.schemas.post import PostsPageResponseSchema
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


@router.get('/{id}/posts', response_model=PostsPageResponseSchema)
async def get_category_posts(
    id: uuid.UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    use_case: GetCategoryPostsUseCase = Depends(get_category_posts_use_case),
    current_user: UserResponseSchema | None = Depends(
        AuthService.get_current_user_or_none
    ),
) -> PostsPageResponseSchema:
    try:
        return await use_case.execute(
            id=id,
            page=page,
            page_size=page_size,
            current_user=current_user,
        )
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
