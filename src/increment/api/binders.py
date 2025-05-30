"""
This module contains definitions of custom binders, used to bind request input
parameters into instances of objects, injected to request handlers.
"""

from blacksheep import FromHeader, Request
from blacksheep.server.bindings import Binder

from increment.domain.common import PageOptions


class IfNoneMatchHeader(FromHeader[str | None]):
    name = "If-None-Match"


class PageOptionsBinder(Binder):
    handle = PageOptions

    async def get_value(self, request: Request) -> PageOptions:
        page = request.query.get("page")
        limit = request.query.get("limit")
        continuation_id = request.query.get("continuation_id")
        if page is None:
            page = 1
        else:
            page = page[0]
        if limit is None:
            limit = 100
        else:
            limit = limit[0]
        if continuation_id is not None:
            continuation_id = int(continuation_id[0])
        return PageOptions(
            page=page,
            limit=limit,
            continuation_id=continuation_id,
        )
