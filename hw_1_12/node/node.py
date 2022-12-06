from dataclasses import dataclass
from typing import List

from aiohttp import web


@dataclass
class NodeNeighborConfig:
    hostname: str
    port: int

    @property
    def url(self):
        return f"http://{self.hostname}:{self.port}"


@dataclass
class NodeConfig:
    name: str
    hostname: str
    port: int
    directory: str
    neighbors: List[NodeNeighborConfig]
    save_files: bool = False


class NodeDaemon:
    def __init__(self, app: web.Application, hostname: str, port: int):
        self._app = app
        self.hostname = hostname
        self.port = port

    async def start(self) -> None:
        runner = web.AppRunner(self._app)
        await runner.setup()
        site = web.TCPSite(runner, self.hostname, self.port)
        await site.start()
