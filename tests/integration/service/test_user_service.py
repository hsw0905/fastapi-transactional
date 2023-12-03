import pytest

from app.exceptions.base_exception import InvalidRequestException
from core.domains.user.dto.user_dto import TransferMoneyDto
from core.domains.user.repository.user_repository import UserRepository
from core.domains.user.service.user_service import TransferMoneyService
from core.persistence.models.user_model import UserModel


def test_should_transfer_money_to_user(test_session):
    user_1 = UserModel(name="Harry", money=10000)
    user_2 = UserModel(name="Ron", money=10000)

    test_session.add_all([user_1, user_2])
    test_session.commit()

    service = TransferMoneyService()
    service.execute(dto=TransferMoneyDto(from_id=user_1.id, to_id=user_2.id, money=2000))

    repository = UserRepository()
    find_user_1 = repository.find_by_id(user_id=user_1.id)
    find_user_2 = repository.find_by_id(user_id=user_2.id)

    assert find_user_1.money == 8000
    assert find_user_2.money == 12000


def test_should_rollback_when_raise_exception(test_session):
    user_1 = UserModel(name="Harry", money=10000)
    user_2 = UserModel(name="exception", money=10000)

    test_session.add_all([user_1, user_2])
    test_session.commit()

    service = TransferMoneyService()
    with pytest.raises(InvalidRequestException):
        service.execute(dto=TransferMoneyDto(from_id=user_1.id, to_id=user_2.id, money=2000))

    repository = UserRepository()
    find_user_1 = repository.find_by_id(user_id=user_1.id)
    find_user_2 = repository.find_by_id(user_id=user_2.id)

    assert find_user_1.money == 10000
    assert find_user_2.money == 10000
