from fastapi import APIRouter, Response, status

router = APIRouter()


@router.get('/hello_world')
async def get_hello_world():
    return Response(content='Hello World!', status_code=status.HTTP_200_OK)
