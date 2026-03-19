from fastapi import APIRouter, HTTPException
from starlette import status
from src.core.exceptions.domain_exceptions import (
    BaseDomainException,
    UserNotFoundByUsernameException,
)
from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.domain.user.use_cases.delete_user_by_username import (
    DeleteUserByUsernameUseCase,
)
from src.domain.user.use_cases.get_user_by_username import (
    GetUserByUsernameUseCase,
)
from src.domain.user.use_cases.update_user_by_username import (
    UpdateUserByUsernameUseCase,
)
from src.schemas.user import UserResponseSchema, UserRequestSchema

user_router = APIRouter()


@user_router.get('/{username}')
async def get_user_by_username(username: str) -> UserResponseSchema:
    use_case = GetUserByUsernameUseCase()
    try:
        user = await use_case.execute(username=username)
    except UserNotFoundByUsernameException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    return user


@user_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(data: UserRequestSchema) -> UserResponseSchema:
    use_case = CreateUserUseCase()
    try:
        user = await use_case.execute(data=data)
    except BaseDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.get_detail()
        )
    return user


@user_router.put('/{username}')
async def update_user_by_username(
    username: str, data: UserRequestSchema
) -> UserResponseSchema:
    use_case = UpdateUserByUsernameUseCase()
    try:
        user = await use_case.execute(username=username, data=data)
    except UserNotFoundByUsernameException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
    except BaseDomainException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=e.get_detail()
        )
    return user


@user_router.delete('/{username}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_username(username: str):
    use_case = DeleteUserByUsernameUseCase()
    try:
        await use_case.execute(username)
    except UserNotFoundByUsernameException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail()
        )
