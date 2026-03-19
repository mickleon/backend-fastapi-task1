import uuid
from pydantic import EmailStr


class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пользователь с id '{id}' не найден"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )

        super().__init__(detail=self._exception_text_template)


class UserNotFoundByUsernameException(BaseDomainException):
    _exception_text_template = "Пользователь с логином '{username}' не найден"

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username
        )

        super().__init__(detail=self._exception_text_template)


class UserUsernameIsNotUniqueException(BaseDomainException):
    _exception_text_template = (
        "Пользователь с логином '{username}' уже существует"
    )

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username
        )

        super().__init__(detail=self._exception_text_template)


class UserEmailIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с email '{email}' уже существует"

    def __init__(self, email: EmailStr) -> None:
        self._exception_text_template = self._exception_text_template.format(
            email=email
        )

        super().__init__(detail=self._exception_text_template)


class CategoryNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Категория с id '{id}' не найдена"

    def __init__(self, id: uuid.UUID) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )

        super().__init__(detail=self._exception_text_template)


class LocationNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Местоположение с id '{id}' не найдено"

    def __init__(self, id: uuid.UUID) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )

        super().__init__(detail=self._exception_text_template)


class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Публикация с id '{id}' не найдена"

    def __init__(self, id: uuid.UUID) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )

        super().__init__(detail=self._exception_text_template)


class CommentNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Комментарий с id '{id}' не найден"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id
        )

        super().__init__(detail=self._exception_text_template)
