from http import HTTPStatus

from fastapi import HTTPException


class InvalidRequestException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=detail)


class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=detail)


class UnAuthorizedException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTPStatus.FORBIDDEN, detail=detail)


class InternalServerErrorException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=detail)
