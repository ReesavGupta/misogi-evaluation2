import uuid
from beanie import Document, Link
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import Field

class TransactionType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"

class User(Document):
    id: UUID = Field(default_factory=uuid.uuid4)
    username: str
    email: str
    password: str
    phone_number: str
    balance: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Transaction(Document):
    id: UUID = Field(default_factory=uuid.uuid4)
    user_id: Link[User] 
    transaction_type: TransactionType = Field(default=TransactionType.CREDIT)
    amount: float = Field(default=0.0)
    description: str = Field(default="")
    reference_transaction_id: Optional[str] = Field(default=None)
    recipient_user_id: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
