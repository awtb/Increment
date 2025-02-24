from typer import Typer

import uvicorn

from increment.app.settings import load_settings

t = Typer()


@t.command("start")
def start():
    settings = load_settings()
    uvicorn.run(
        "increment.app.main:app", host=settings.serving.host, port=settings.serving.port
    )


t()
