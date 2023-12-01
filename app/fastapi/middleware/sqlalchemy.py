from starlette.types import ASGIApp, Receive, Scope, Send

from app.database.sqlalchemy import session
from app.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class SqlalchemyMiddleware:
    def __init__(self, app: ASGIApp):
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            await self._app(scope, receive, send)
        except Exception as e:
            logger.error(f"[SqlalchemyMiddleware] - error: {e}")
        finally:
            session.remove()
