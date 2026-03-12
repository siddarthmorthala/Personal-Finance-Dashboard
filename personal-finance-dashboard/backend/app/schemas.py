from datetime import date
from pydantic import BaseModel


class TransactionOut(BaseModel):
    id: int
    date: date
    description: str
    amount: float
    category: str

    model_config = {"from_attributes": True}
