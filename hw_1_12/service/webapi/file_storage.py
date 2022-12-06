from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError


class DistributedFileStorage:
    def __init__(self, url):
        self.url = url

    async def get(self, filename: str) -> str:
        async with ClientSession() as session:
            try:
                async with session.get(f"{self.url}/{filename}") as response:
                    if response.status == 404:
                        raise FileNotFoundError
                    return await response.text()
            except ClientConnectorError:
                raise FileNotFoundError
