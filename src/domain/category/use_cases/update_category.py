import uuid
from fastapi import HTTPException

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
            category = self._repo.get(session=session, id=id)

            if category is None:
                raise HTTPException(
                    status_code=404, detail=f'Категория с id "{id}" не найдена'
                )

            self._repo.update(session=session, category=category, data=data)

        return CategoryResponseSchema.model_validate(obj=category)
