from datetime import datetime
from typing import Optional
# import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from models.model import Transaction, TransactionType, User 
from uuid import UUID

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/{user_id}/page={page}/limit={limit}")
async def get_user_transactions(user_id: str, page : str, limit: str):
    user_id = UUID(user_id)
    
    page = int(page)
    limit = int(limit)

    transactions = await Transaction.find(Transaction.user_id == user_id).skip((page - 1) * limit).limit(limit).to_list()
    
    if not transactions:
        raise HTTPException(status_code=404, detail="Transactions not found")
    return {
        "transactions": [transaction.model_dump() for transaction in transactions],
        "total": len(transactions),
        "page": page,
        "limit": limit
    }

@router.get("/detail/{transaction_id}")
async def get_transaction_detail(transaction_id: str):
    transaction_id = UUID(transaction_id)
    transaction = await Transaction.find_one(Transaction.id == transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction.model_dump()


class ICreateTransaction(BaseModel):
    user_id: str
    transaction_type: TransactionType
    amount: float
    description: str
    reference_transaction_id: Optional[str] = None
    recipient_user_id: Optional[str] = None

@router.post("/")
async def create_transaction(transaction: ICreateTransaction):
    # TypeError: 'UUID' object has no attribute 'replace'
    transaction.user_id = transaction.user_id
    
    if transaction.reference_transaction_id:
        transaction.reference_transaction_id = UUID(transaction.reference_transaction_id)
    if transaction.recipient_user_id:
        transaction.recipient_user_id = transaction.recipient_user_id
        
    print("--------------------------------")
    print("user_id: ",  transaction.user_id)    
    print("reference_transaction_id: ",  transaction.reference_transaction_id)
    print("recipient_user_id: ",  transaction.recipient_user_id)
    print("--------------------------------")

    user = await User.find_one(User.id == transaction.user_id)
    print("user: ", user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if transaction.transaction_type == TransactionType.CREDIT:
        user.balance += transaction.amount
    elif transaction.transaction_type == TransactionType.DEBIT:
        user.balance -= transaction.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    user.updated_at = datetime.now()

    transaction = Transaction(
        user_id=user,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount,
        description=transaction.description,
        reference_transaction_id=transaction.reference_transaction_id,
        recipient_user_id=transaction.recipient_user_id
    )
    
    await user.save()
    
    await transaction.save()
    
    return transaction.model_dump()
