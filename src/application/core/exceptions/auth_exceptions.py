from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self, detail: str) -> None:
        self.detail = detail

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={'WWW-Authenticate': 'Bearer'},
        )


class AccessDeniedException(HTTPException):
    _detail = 'Недостаточно прав'

    def __init__(self) -> None:
        self.detail = self._detail

        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=self.detail,
        )
