from sqlalchemy import VARCHAR, DECIMAL
from sqlalchemy.orm import mapped_column

from core.persistence.models.base import Base
from core.persistence.models.base_time import BaseTimeModel


class UserModel(Base, BaseTimeModel):
    __tablename__ = "users"

    name = mapped_column(VARCHAR(20), nullable=False)
    money = mapped_column(DECIMAL(precision=10, scale=2))
