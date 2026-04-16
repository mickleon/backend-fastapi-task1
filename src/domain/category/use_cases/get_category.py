import logging
import uuid

from src.core.exceptions.database_exceptions import CategoryNotFoundException
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.schemas.category import CategoryResponseSchema
from src.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class GetCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self,
        id: uuid.UUID,
        current_user: UserResponseSchema | None,
    ) -> CategoryResponseSchema:
        with self._database.session() as session:
            try:
                category = self._repo.get(session=session, id=id)
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=id)
                username = (
                    current_user.username
                    if current_user is not None
                    else 'анонимный'
                )
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error
            return CategoryResponseSchema.model_validate(obj=category)
