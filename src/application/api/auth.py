from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from application.schemas.auth import Token
from application.domain.auth.use_cases.authenticate_user import (
    AuthenticateUserUseCase,
)
from application.domain.auth.use_cases.create_access_token import (
    CreateAccessTokenUseCase,
)
from application.core.exceptions.domain_exceptions import (
    WrongUsernameOrPasswordException,
)
from application.api.depends import (
    create_access_token_use_case,
    authenticate_user_use_case,
)

router = APIRouter()


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: Annotated[
        AuthenticateUserUseCase, Depends(authenticate_user_use_case)
    ],
    create_token_use_case: CreateAccessTokenUseCase = Depends(
        create_access_token_use_case
    ),
) -> Token:
    try:
        user = await auth_use_case.execute(
            username=form_data.username, password=form_data.password
        )
    except WrongUsernameOrPasswordException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.get_detail(),
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = await create_token_use_case.execute(username=user.username)

    return Token(access_token=access_token, token_type='bearer')
