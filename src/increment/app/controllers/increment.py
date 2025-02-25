from blacksheep.server.controllers import Controller, get, post, APIController


class IncrementController(APIController):
    @classmethod
    def version(cls) -> str:
        return "v1"

    @classmethod
    def class_name(cls) -> str:
        return "increment"

    @post()
    async def increment(self):
        """
        Slower version of increment, v1
        """


class IncrementControllerV2(APIController):
    @classmethod
    def version(cls) -> str:
        return "v2"

    @classmethod
    def class_name(cls) -> str:
        return "increment"

    @post()
    async def increment(self):
        """
        Faster version of increment, v2
        """
