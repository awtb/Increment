from typing import Tuple

from rodi import Container

from increment.api.settings import Settings


def configure_services(settings: Settings) -> Tuple[Container, Settings]:
    container = Container()

    container.add_instance(settings)

    return container, settings
