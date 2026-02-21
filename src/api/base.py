from fastapi import APIRouter

from src.schemas.blog import User, Category

router = APIRouter()


@router.post('/category/add')
async def category_add(category: Category) -> dict:
    return {'category': category.slug, 'created_at': category.created_at}
