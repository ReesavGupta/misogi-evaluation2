from datetime import datetime
from uuid import UUID
from typing import Optional
import beanie
from models.model import Transaction, TransactionType, User
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
router = APIRouter(prefix="/transfer", tags=["transfer"])

class ITransferCreate(BaseModel):
    sender_user_id: str
    recipient_user_id: str
    amount: float
    description: str

@router.post("/")
async def transfer(transfer: ITransferCreate):
    
    # print("transfer: ", transfer)
    sender = await User.find_one(User.id == UUID(transfer.sender_user_id))
    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")
    recipient = await User.find_one(User.id == UUID(transfer.recipient_user_id))
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    if sender.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    # print("sender: ", sender)
    sender.balance -= transfer.amount
    recipient.balance += transfer.amount
    sender.updated_at = datetime.now()
    recipient.updated_at = datetime.now()
    await sender.save()
    await recipient.save()
    import bson
# ValueError: cannot encode native uuid.UUID with UuidRepresentation.UNSPECIFIED. UUIDs can be manually converted to bson.Binary instances using bson.Binary.from_uuid()
    transaction = Transaction(
        user_id=sender,
        transaction_type=TransactionType.TRANSFER_OUT,
        amount=transfer.amount,
        description=transfer.description,
        recipient_user_id=str(recipient.id),
        reference_transaction_id=None
    )

    print("transaction: ", transaction)
    recipient_transaction = Transaction(
        user_id=recipient,
        transaction_type=TransactionType.TRANSFER_IN,
        amount=transfer.amount,
        description=transfer.description,
        # reference_transaction_id=transaction.id,
        recipient_user_id=str(recipient.id),
        reference_transaction_id=bson.Binary.from_uuid(transaction.id)
    )

    print("recipient_transaction: ", recipient_transaction)

    await transaction.save()
    await recipient_transaction.save()

    return {
        "transfer_id": transaction.id,
        "sender_transaction_id": transaction.id,
        "recipient_transaction_id": recipient_transaction.id,
        "amount": transfer.amount,
        "sender_new_balance": sender.balance,
        "recipient_new_balance": recipient.balance,
        "status": "completed"
    }


@router.get("/{transfer_id}")
async def get_transfer(transfer_id: UUID):
    transaction = await Transaction.find_one(Transaction.id  == transfer_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return {
        "transfer_id": transaction.id,
        "sender_user_id": transaction.user_id.id,
        "recipient_user_id": transaction.recipient_user_id,
        "amount": transaction.amount,
        "description": transaction.description,
        "status": transaction.status,
        "reference_transaction_id": transaction.reference_transaction_id,
        "created_at": transaction.created_at
    }