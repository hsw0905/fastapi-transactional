from sqlalchemy import select, update

from app.database.sqlalchemy import session
from core.persistence.models.user_model import UserModel


class UserRepository:
    def save(self, user: UserModel) -> None:
        session.add(user)

    def find_by_id(self, user_id: int) -> UserModel | None:
        statement = (
            select(UserModel).where(UserModel.id == user_id)
        )

        return session.execute(statement).scalar()

    def update(self, user_id: int, money: int) -> None:
        statement = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(money=money)
        )

        session.execute(statement)
