import inject

from app.database.transactional import Transactional
from app.exceptions.base_exception import InvalidRequestException
from core.domains.user.dto.user_dto import TransferMoneyDto
from core.domains.user.repository.user_repository import UserRepository
from core.persistence.models.user_model import UserModel


class TransferMoneyService:
    @inject.autoparams()
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    @Transactional()
    def execute(self, dto: TransferMoneyDto):
        from_user = self._user_repo.find_by_id(dto.from_id)
        to_user = self._user_repo.find_by_id(dto.to_id)

        self._user_repo.update(user_id=from_user.id, money=from_user.money - dto.money)
        self._validate_something(to_user)
        self._user_repo.update(user_id=to_user.id, money=to_user.money + dto.money)

    def _validate_something(self, to_user: UserModel):
        if to_user.name == "exception":
            raise InvalidRequestException(detail="some exception")
