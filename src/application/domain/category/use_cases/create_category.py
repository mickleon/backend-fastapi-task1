from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.category import (
    CategoryRepository,
)
from application.schemas.category import (
    CategoryRequestSchema,
    CategoryResponseSchema,
)
from application.schemas.user import UserResponseSchema


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, data: CategoryRequestSchema, current_user: UserResponseSchema
    ) -> CategoryResponseSchema:
        async with self._database.session() as session:
            category = await self._repo.create(session=session, data=data)

            return CategoryResponseSchema.model_validate(obj=category)
