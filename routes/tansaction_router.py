from datetime import datetime
from fastapi import APIRouter, HTTPException
from models.model import Transaction, TransactionType

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/{user_id}?page={page}&limit={limit}")
async def get_user_transactions(user_id: str, page : int, limit: int):
    transactions = await Transaction.find(Transaction.user_id == user_id).skip((page - 1) * limit).limit(limit)
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
    transaction = await Transaction.find_one(Transaction.id == transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction.model_dump()


@router.post("/")
async def create_transaction(transaction: Transaction):
    if transaction.transaction_type == TransactionType.CREDIT:
        transaction.user_id.balance += transaction.amount
    elif transaction.transaction_type == TransactionType.DEBIT:
        transaction.user_id.balance -= transaction.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    transaction.user_id.updated_at = datetime.now()
    
    await transaction.user_id.save()
    
    await transaction.save()
    
    return transaction.model_dump()
