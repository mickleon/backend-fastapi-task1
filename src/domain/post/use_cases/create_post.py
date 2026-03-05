from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.post import Post
from src.infrastructure.sqlite.repositories.post import PostRepository
from src.schemas.post import PostRequestSchema, PostResponseSchema


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, data: PostRequestSchema):
        with self._database.session() as session:
            post = Post(**data.model_dump())
            self._repo.create(session=session, post=post)

        return PostResponseSchema.model_validate(obj=post)

