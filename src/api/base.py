from fastapi import APIRouter

from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.domain.user.use_cases.delete_user_by_username import (
    DeleteUserByUsernameUseCase,
)
from src.domain.user.use_cases.get_user_by_username import GetUserByUsernameUseCase
from src.domain.user.use_cases.update_user_by_username import (
    UpdateUserByUsernameUseCase,
)
from src.schemas.user import UserResponseSchema, UserRequestSchema

router = APIRouter()


@router.get('/user/{login}')
async def get_user_by_username(username: str) -> UserResponseSchema:
    use_case = GetUserByUsernameUseCase()
    return await use_case.execute(username=username)


@router.post('/user')
async def create_user(data: UserRequestSchema) -> UserResponseSchema:
    use_case = CreateUserUseCase()
    return await use_case.execute(data=data)


@router.put('/user/{login}')
async def update_user_by_username(
    username: str, data: UserRequestSchema
) -> UserResponseSchema:
    use_case = UpdateUserByUsernameUseCase()
    return await use_case.execute(username=username, data=data)


@router.delete('/user/{login}')
async def delete_user_by_username(login: str) -> dict:
    use_case = DeleteUserByUsernameUseCase()
    await use_case.execute(login)

    return {'message': f'Пользователь "{login}" успешно удален'}
