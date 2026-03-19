from fastapi import APIRouter
from starlette import status
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
    return await use_case.execute(username=username)


@user_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(data: UserRequestSchema) -> UserResponseSchema:
    use_case = CreateUserUseCase()
    return await use_case.execute(data=data)


@user_router.put('/{username}')
async def update_user_by_username(
    username: str, data: UserRequestSchema
) -> UserResponseSchema:
    use_case = UpdateUserByUsernameUseCase()
    return await use_case.execute(username=username, data=data)


@user_router.delete('/{username}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_username(username: str):
    use_case = DeleteUserByUsernameUseCase()
    await use_case.execute(username)
    return {'message': f'Пользователь "{username}" успешно удален'}
