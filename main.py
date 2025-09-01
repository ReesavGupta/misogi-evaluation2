import uvicorn
from fastapi import FastAPI
from db.db import init_db
from contextlib import asynccontextmanager
from routes.user_router import router as user_router
from routes.wallet_router import router as wallet_router
from routes.tansaction_router import router as transaction_router
from routes.transfer_router import router as transfer_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(wallet_router)
app.include_router(transaction_router)
app.include_router(transfer_router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)