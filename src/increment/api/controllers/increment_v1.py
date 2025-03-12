from blacksheep.server.controllers import APIController, post


class IncrementController(APIController):
    @classmethod
    def version(cls) -> str:
        return "v2"

    @classmethod
    def class_name(cls) -> str:
        return "increment"

    @post()
    async def increment(self):
        """Fast version of Increment API, v2"""
        raise NotImplementedError()
