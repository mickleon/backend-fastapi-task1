class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundByUsernameException(BaseDomainException):
    _exception_text_template = "Пользователь с логином='{username}' не найден"

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username
        )

        super().__init__(detail=self._exception_text_template)


class UserUsernameIsNotUniqueException(BaseDomainException):
    _exception_text_template = (
        "Пользователь с логином='{username}' уже существует"
    )

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username
        )

        super().__init__(detail=self._exception_text_template)
