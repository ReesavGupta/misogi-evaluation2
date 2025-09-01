from uuid import UUID
from datetime import datetime
from models.model import User
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

class IupdateUser(BaseModel):
    username: str
    phone_number: str
    # Response: 200 OK


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}")
async def get_user(user_id: UUID):
    user = await User.find_one(User.id == user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "balance": user.balance,
        "created_at": user.created_at
    }


@router.put("/{user_id}")
async def update_user(user_id: UUID, user: IupdateUser):
    updated_user =await User.find_one(User.id == user_id)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user.updated_at = datetime.now()
    
    if updated_user.username != user.username:
        updated_user.username = user.username
    if updated_user.phone_number != user.phone_number:
        updated_user.phone_number = user.phone_number
        
    await updated_user.save()
    
    return updated_user