from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.category import Category
from src.infrastructure.sqlite.repositories.category import CategoryRepository
from src.schemas.category import CategoryRequestSchema, CategoryResponseSchema


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, data: CategoryRequestSchema):
        with self._database.session() as session:
            category = Category(**data.model_dump())
            self._repo.create(session=session, category=category)
            return CategoryResponseSchema.model_validate(obj=category)
