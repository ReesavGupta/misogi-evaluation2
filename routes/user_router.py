from uuid import UUID
from datetime import datetime
from models.model import User
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

class IupdateUser(BaseModel):
    username: str
    phone_number: str

class ICreateUser(BaseModel):
    username: str
    email: str
    password: str
    phone_number: str

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

@router.post("/")
async def create_user(user: ICreateUser):
    user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        phone_number=user.phone_number,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        balance=0
    )

    print(user)
    # id=None revision_id=None username='reesav' email='email@reesav.com' password='123456789' phone_number='987654345' balance=0.0 created_at=datetime.datetime(2025, 9, 1, 17, 26, 46, 381965) updated_at=datetime.datetime(2025, 9, 1, 17, 26, 46, 381965)
    await user.save()
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