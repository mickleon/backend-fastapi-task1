import uuid

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.schemas.category import CategoryResponseSchema


class GetCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, id: uuid.UUID) -> CategoryResponseSchema:
        with self._database.session() as session:
            category = self._repo.get(session=session, id=id)
            return CategoryResponseSchema.model_validate(obj=category)

