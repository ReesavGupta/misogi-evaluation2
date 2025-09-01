from uuid import UUID
from models.model import TransactionType, User
from datetime import datetime
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/wallet", tags=["wallet"])

@router.get("/{user_id}/balance")
async def get_balance(user_id: str):
    user_id = UUID(user_id)
    user = await User.find_one(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.id,
        "balance": user.balance,
        "last_updated": user.updated_at
    }

@router.post("/{user_id}/add-money")
async def add_money(user_id: str, amount: float, description: str):
    user_id = UUID(user_id)
    user = await User.find_one(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.balance += amount
    user.updated_at = datetime.now()
    await user.save()
    return {
        "transaction_id": user.id,
        "user_id": user.id,
        "amount": amount,
        "new_balance": user.balance,
        "transaction_type": TransactionType.CREDIT
    }

@router.post("/{user_id}/withdraw")
async def withdraw(user_id: str, amount: float, description: str):
    user_id = UUID(user_id)
    user = await User.find_one(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.balance -= amount
    user.updated_at = datetime.now()
    await user.save()
    return {
        "transaction_id": user.id,
        "user_id": user.id,
        "amount": amount,
        "new_balance": user.balance,
        "transaction_type": TransactionType.DEBIT
    }