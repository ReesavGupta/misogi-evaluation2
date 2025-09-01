import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv
from models.model import User, Transaction

load_dotenv()

mongo_uri = os.getenv("MONGODB_URI")
mongo_db_name = os.getenv("MONGO_DB_NAME")

client: AsyncIOMotorClient | None = None

async def init_db():
    try:

        global client

        client = AsyncIOMotorClient(mongo_uri)
        
        if not mongo_db_name:
            raise Exception("MONGO_DB_NAME is not set")
        
        db=client[mongo_db_name]

        await init_beanie(database=db, document_models=[User, Transaction])

    except Exception as e:
        print(f"Error initializing MongoDB: {e}")
        raise e