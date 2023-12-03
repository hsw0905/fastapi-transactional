from pydantic import BaseModel


class TransferMoneyDto(BaseModel):
    from_id: int
    to_id: int
    money: int
