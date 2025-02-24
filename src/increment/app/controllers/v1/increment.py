"""
Example API implemented using a controller.
"""

from typing import List, Optional

from blacksheep.server.controllers import Controller, get, post


class IncrementController(Controller):
    @classmethod
    def route(cls) -> Optional[str]:
        return "/api/v1/increment"

    @classmethod
    def class_name(cls) -> str:
        return "Increment"

    @post()
    async def increment(self):
        return "HELLO"
