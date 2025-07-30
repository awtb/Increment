from blacksheep import JSONContent, Response
from blacksheep.server.controllers import APIController, get


class SystemController(APIController):
    @classmethod
    def version(cls) -> str:
        return "v1"

    @classmethod
    def class_name(cls) -> str:
        return "System"

    @get()
    async def get_health_status(self) -> Response:
        """Health-checking endpoint"""
        content = JSONContent({"healthy": True})
        return Response(status=200, content=content)

    @get()
    async def is_system_ready(self) -> Response:
        """Is system ready to accept requests"""
        content = JSONContent({"ready": True})
        return Response(content=content, status=200)
