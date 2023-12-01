from inject import Binder, clear_and_configure


def configure_app(binder: Binder) -> None:
    service_to_bind = []

    for service in service_to_bind:
        binder.bind_to_provider(service, service)


def init_provider() -> None:
    clear_and_configure(configure_app)