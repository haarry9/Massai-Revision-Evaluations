from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]

users_collection = db["users"]
movies_collection = db["movies"]
theatres_collection = db["theaters"]
screens_collection = db["screens"]
shows_collection = db["shows"]
bookings_collection = db["bookings"]