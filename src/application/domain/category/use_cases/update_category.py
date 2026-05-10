import logging
import uuid

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.category import (
    CategoryRepository,
)
from application.schemas.category import (
    CategoryRequestSchema,
    CategoryResponseSchema,
)
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self,
        id: uuid.UUID,
        data: CategoryRequestSchema,
        current_user: UserResponseSchema,
    ) -> CategoryResponseSchema:
        async with self._database.session() as session:
            try:
                category = await self._repo.update(
                    session=session, id=id, data=data
                )
            except CategoryNotFoundException:
                error = CategoryNotFoundByIdException(id=id)
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error

            return CategoryResponseSchema.model_validate(obj=category)
