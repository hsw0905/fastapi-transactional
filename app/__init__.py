from fastapi import FastAPI

from app.config import config
from app.dependency.ioc_container import init_provider


# def init_routers(app_: FastAPI):
#     app_.include_router(v1_router)


def create_app() -> FastAPI:
    fastapi = FastAPI(
        debug=config.DEBUG,
        app_host=config.APP_HOST,
        app_port=config.APP_PORT,
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
    )

    init_provider()
    # init_routers(fastapi)

    print(f"\n💌💌💌FastAPI Config is '{config.ENV}'")

    return fastapi


app: FastAPI = create_app()
