from typing import Annotated
from fastapi import APIRouter, HTTPException, Path
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from src.schemas.blog import Category, SLUG_PATTERN

router = APIRouter()

categories: list[Category] = [
    Category(title='Путешествия', description='Все о путешествиях', slug='travel'),
    Category(title='Рок-музыка', description='Все о рок-музыке', slug='rock-music'),
]


@router.get('/category/{category_slug}')
async def get_category(
    category_slug: Annotated[str, Path(pattern=SLUG_PATTERN)],
) -> Category:
    for category in categories:
        if category.slug == category_slug:
            return category
    raise HTTPException(status_code=404, detail=f'Category "{category_slug}" not found')


@router.post('/category')
async def add_category(category_to_add: Category) -> dict:
    slug_to_add = category_to_add.slug
    for category in categories:
        if category.slug == slug_to_add:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT,
                detail=f'Category "{slug_to_add}" already exists',
            )
    categories.append(category_to_add)
    return {'message': f'Category "{slug_to_add}" created successfully!'}


@router.put('/category/{category_slug}')
async def update_category(
    category_slug: Annotated[str, Path(pattern=SLUG_PATTERN)],
    category_new: Category,
) -> dict:
    for index, category in enumerate(categories):
        if category.slug == category_slug:
            categories[index] = category_new
            return {'message': f'Category "{category_slug}" updated successfully!'}
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f'Category "{category_slug}" not found',
    )


@router.delete('/category/{category_slug}')
async def delete_category(
    category_slug: Annotated[str, Path(pattern=SLUG_PATTERN)],
) -> dict:
    for category in categories:
        if category.slug == category_slug:
            categories.remove(category)
            return {'message': f'Category "{category.slug}" deleted successfully!'}
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND, detail=f'Category "{category_slug}" not found'
    )
