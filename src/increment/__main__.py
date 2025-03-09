import uvicorn
from typer import Option, Typer

from increment.app.settings import load_settings

t = Typer()


@t.command("start")
def start(
    reload: bool = Option(default=False, help="Reload on code changes?"),
):
    settings = load_settings()
    uvicorn.run(
        "increment.app.main:app",
        host=settings.serving_host,
        port=settings.serving_port,
        reload=reload,
    )


t()
