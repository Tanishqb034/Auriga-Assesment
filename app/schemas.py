from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class BorrowerCreate(BaseModel):
    name: str
    email: EmailStr


class RentalCreate(BaseModel):
    borrower_id: int
    equipment_id: int
    quantity: int
    borrow_date: date
    due_date: date
    deposit: float


class RentalReturn(BaseModel):
    return_date: date

class RentalTransfer(BaseModel):
    new_borrower_id: int