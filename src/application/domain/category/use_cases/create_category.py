import logging
from application.core.exceptions.auth_exceptions import AccessDeniedException
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


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, data: CategoryRequestSchema, current_user: UserResponseSchema
    ) -> CategoryResponseSchema:
        if not current_user.is_admin:
            error = AccessDeniedException()
            logger.error(
                f'Доступ запрещен: пользователь {current_user.username} попытался создать категорию'
            )
            raise error
        async with self._database.session() as session:
            category = await self._repo.create(session=session, data=data)

            return CategoryResponseSchema.model_validate(obj=category)
