from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
from src.api.depends import (
    delete_user_by_username_use_case,
    get_user_by_username_use_case,
    get_user_posts_by_username_use_case,
    create_user_use_case,
    update_user_by_username_use_case,
)
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByUsernameException,
    UserUsernameOrEmailIsNotUniqueException,
)
from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.domain.user.use_cases.delete_user_by_username import (
    DeleteUserByUsernameUseCase,
)
from src.domain.user.use_cases.get_user_by_username import (
    GetUserByUsernameUseCase,
)
from src.domain.user.use_cases.get_user_posts_by_username import (
    GetUserPostsByUsernameUseCase,
)
from src.domain.user.use_cases.update_user_by_username import (
    UpdateUserByUsernameUseCase,
)
from src.schemas.post import PostsPageResponseSchema
from src.schemas.user import UserResponseSchema, UserRequestSchema

user_router = APIRouter()


@user_router.get('/{username}')
async def get_user_by_username(
    username: str,
    use_case: GetUserByUsernameUseCase = Depends(
        get_user_by_username_use_case
    ),
) -> UserResponseSchema:
    try:
        return await use_case.execute(username=username)
    except UserNotFoundByUsernameException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@user_router.get('/{username}/posts')
async def get_user_posts_by_username(
    username: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    use_case: GetUserPostsByUsernameUseCase = Depends(
        get_user_posts_by_username_use_case
    ),
) -> PostsPageResponseSchema:
    try:
        return await use_case.execute(
            username=username, page=page, page_size=page_size
        )
    except UserNotFoundByUsernameException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )


@user_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserRequestSchema,
    use_case: CreateUserUseCase = Depends(create_user_use_case),
) -> UserResponseSchema:
    try:
        return await use_case.execute(data=data)
    except UserUsernameOrEmailIsNotUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.get_detail()
        )


@user_router.put('/{username}')
async def update_user_by_username(
    username: str,
    data: UserRequestSchema,
    use_case: UpdateUserByUsernameUseCase = Depends(
        update_user_by_username_use_case
    ),
) -> UserResponseSchema:
    try:
        return await use_case.execute(username=username, data=data)
    except UserNotFoundByUsernameException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except UserUsernameOrEmailIsNotUniqueException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.get_detail()
        )


@user_router.delete('/{username}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_username(
    username: str,
    use_case: DeleteUserByUsernameUseCase = Depends(
        delete_user_by_username_use_case
    ),
):
    try:
        return await use_case.execute(username)
    except UserNotFoundByUsernameException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
