from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.post import PostRequestSchema, PostResponseSchema


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, data: PostRequestSchema):
        with self._database.session() as session:
            post = self._repo.create(session=session, data=data)

            return PostResponseSchema.model_validate(obj=post)
