import asyncio
import uvicorn

from src.app import create_app
from src.core.config import settings

app = create_app()


async def main() -> None:
    config = uvicorn.Config(
        'main:app',
        host='0.0.0.0',
        port=settings.PORT,
    )
    server = uvicorn.Server(config=config)
    tasks = (asyncio.create_task(server.serve()),)

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
