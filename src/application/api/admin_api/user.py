from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from application.api.depends import (
    delete_user_by_username_use_case,
    get_user_by_username_admin_use_case,
    get_user_posts_by_username_admin_use_case,
    update_user_by_username_admin_use_case,
)
from application.core.exceptions.domain_exceptions import (
    UserNotFoundByUsernameException,
    UserUsernameOrEmailIsNotUniqueException,
)
from application.domain.user.use_cases.delete_user_by_username import (
    DeleteUserByUsernameUseCase,
)
from application.domain.user.use_cases.get_user_by_username_admin import (
    GetUserByUsernameAdminUseCase,
)
from application.domain.user.use_cases.get_user_posts_by_username_admin import (
    GetUserPostsByUsernameAdminUseCase,
)
from application.domain.user.use_cases.update_user_by_username_admin import (
    UpdateUserByUsernameAdminUseCase,
)
from application.schemas.post import PostsPageResponseSchema
from application.schemas.user import UserRequestSchema, UserResponseSchema
from application.services.auth import AuthService

router = APIRouter()


@router.get('/{username}', response_model=UserResponseSchema)
async def get_user_by_username_admin(
    username: str,
    use_case: GetUserByUsernameAdminUseCase = Depends(
        get_user_by_username_admin_use_case
    ),
    current_user: UserResponseSchema | None = Depends(
        AuthService.require_admin
    ),
) -> UserResponseSchema:
    try:
        return await use_case.execute(
            target_username=username, current_user=current_user
        )
    except UserNotFoundByUsernameException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.get('/{username}/posts', response_model=PostsPageResponseSchema)
async def get_user_posts_by_username_admin(
    username: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    use_case: GetUserPostsByUsernameAdminUseCase = Depends(
        get_user_posts_by_username_admin_use_case
    ),
    current_user: UserResponseSchema | None = Depends(
        AuthService.require_admin
    ),
) -> PostsPageResponseSchema:
    try:
        return await use_case.execute(
            target_username=username,
            page=page,
            page_size=page_size,
            current_user=current_user,
        )
    except UserNotFoundByUsernameException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@router.put(
    '/{username}',
    response_model=UserResponseSchema,
)
async def update_user_by_username_admin(
    username: str,
    data: UserRequestSchema,
    use_case: UpdateUserByUsernameAdminUseCase = Depends(
        update_user_by_username_admin_use_case
    ),
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
) -> UserResponseSchema:
    try:
        return await use_case.execute(
            target_username=username, data=data, current_user=current_user
        )
    except UserNotFoundByUsernameException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except UserUsernameOrEmailIsNotUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.get_detail()
        )


@router.delete(
    '/{username}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_by_username_admin(
    username: str,
    current_user: UserResponseSchema = Depends(AuthService.require_admin),
    use_case: DeleteUserByUsernameUseCase = Depends(
        delete_user_by_username_use_case
    ),
):
    try:
        return await use_case.execute(
            target_username=username, current_user=current_user
        )
    except UserNotFoundByUsernameException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
