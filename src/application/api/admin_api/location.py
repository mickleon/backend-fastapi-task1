import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status

from application.api.depends import (
    create_location_use_case,
    delete_location_use_case,
    get_location_admin_use_case,
    get_location_posts_admin_use_case,
    update_location_use_case,
)
from application.core.exceptions.domain_exceptions import (
    LocationNotFoundByIdException,
)
from application.domain.location.use_cases.create_location import (
    CreateLocationUseCase,
)
from application.domain.location.use_cases.delete_location import (
    DeleteLocationUseCase,
)
from application.domain.location.use_cases.get_location_admin import (
    GetLocationAdminUseCase,
)
from application.domain.location.use_cases.get_location_posts_admin import (
    GetLocationPostsAdminUseCase,
)
from application.domain.location.use_cases.update_location import (
    UpdateLocationUseCase,
)
from application.schemas.location import (
    LocationRequestSchema,
    LocationResponseSchema,
)
from application.schemas.post import PostsPageResponseSchema
from application.schemas.user import UserResponseSchema
from application.services.auth import AuthService

router = APIRouter()


@router.get('/{id}', response_model=LocationResponseSchema)
async def get_location_admin(
    id: uuid.UUID,
    use_case: GetLocationAdminUseCase = Depends(get_location_admin_use_case),
    current_user: UserResponseSchema | None = Depends(
        AuthService.require_admin
    ),
) -> LocationResponseSchema:
    try:
        return await use_case.execute(id=id, current_user=current_user)
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.get('/{id}/posts', response_model=PostsPageResponseSchema)
async def get_location_posts_admin(
    id: uuid.UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    use_case: GetLocationPostsAdminUseCase = Depends(
        get_location_posts_admin_use_case
    ),
    current_user: UserResponseSchema | None = Depends(
        AuthService.require_admin
    ),
) -> PostsPageResponseSchema:
    try:
        return await use_case.execute(
            id=id,
            page=page,
            page_size=page_size,
            current_user=current_user,
        )
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=LocationResponseSchema,
)
async def create_location_admin(
    data: LocationRequestSchema,
    use_case: CreateLocationUseCase = Depends(create_location_use_case),
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
) -> LocationResponseSchema:
    return await use_case.execute(data=data, current_user=current_user)


@router.put(
    '/{id}',
    response_model=LocationResponseSchema,
)
async def update_location_admin(
    id: uuid.UUID,
    data: LocationRequestSchema,
    use_case: UpdateLocationUseCase = Depends(update_location_use_case),
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
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
async def delete_location_admin(
    id: uuid.UUID,
    use_case: DeleteLocationUseCase = Depends(delete_location_use_case),
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
):
    try:
        await use_case.execute(id, current_user=current_user)
    except LocationNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
