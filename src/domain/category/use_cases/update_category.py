import uuid

from src.core.exceptions.database_exceptions import CategoryNotFoundException
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException
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
            try:
                category = self._repo.update(session=session, id=id, data=data)
            except CategoryNotFoundException:
                raise CategoryNotFoundByIdException(id=id)

            return CategoryResponseSchema.model_validate(obj=category)
