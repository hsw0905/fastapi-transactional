from enum import Enum
from functools import wraps
from app.utils.log_helper import logger_

from app.database.sqlalchemy import session

logger = logger_.getLogger(__name__)


class Propagation(Enum):
    REQUIRED = "required"
    REQUIRED_NEW = "required_new"


class Transactional:
    def __init__(self, propagation: Propagation = Propagation.REQUIRED):
        self._propagation = propagation

    def __call__(self, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                result = self._run_required(function=function, args=args, kwargs=kwargs)
                return result
            except Exception as e:
                session.rollback()
                raise e

        return wrapper

    def _run_required(self, function, args, kwargs):
        result = function(*args, **kwargs)
        session.commit()
        return result
