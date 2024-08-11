import asyncio

from finder_service.code.service import Service


async def main():
    service = Service()
    await service.run()


if __name__ == '__main__':
    asyncio.run(main())