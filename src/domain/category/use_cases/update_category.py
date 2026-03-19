import uuid

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.schemas.category import CategoryRequestSchema, CategoryResponseSchema


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(
        self, id: uuid.UUID, data: CategoryRequestSchema
    ) -> CategoryResponseSchema:
        with self._database.session() as session:
            category = self._repo.update(session=session, id=id, data=data)

            return CategoryResponseSchema.model_validate(obj=category)
