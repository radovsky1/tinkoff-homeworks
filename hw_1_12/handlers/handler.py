from aiohttp import web
from hw_1_12.service import ServiceInterface


class Handler:
    def __init__(self, service: ServiceInterface):
        self.service = service

    def init_routes(self, app: web.Application):
        app.router.add_get("/{file_name}", self.get_file)

    async def get_file(self, request: web.Request) -> web.Response:
        file_name = request.match_info["file_name"]
        try:
            file_content = await self.service.get_file(file_name)
        except FileNotFoundError:
            return web.Response(status=404)
        return web.Response(text=file_content)
