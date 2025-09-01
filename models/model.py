from beanie import Document, Link
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

class TransactionType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"

class User(Document):
    username: str
    email: str
    password: str
    phone_number: str
    balance: float
    created_at: datetime
    updated_at: datetime


class Transaction(Document):
    user_id: Link[User]
    transaction_type: TransactionType
    amount: float
    description: str
    reference_transaction_id: Optional[UUID]
    recipient_user_id: Optional[Link[User]]
    created_at: datetime
