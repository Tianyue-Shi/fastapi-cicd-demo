import os

from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "fastapi_demo"

client: AsyncIOMotorClient = None
db = None


async def connect_to_mongo():
    """Create the MongoDB client and connect to the database."""
    global client, db
    try:
        client = AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
        db = client[DATABASE_NAME]
        # Verify connectivity (will raise if MongoDB is unreachable)
        await client.server_info()
        print(f"Connected to MongoDB at {MONGODB_URL}")
    except Exception as e:
        print(f"WARNING: Could not connect to MongoDB at {MONGODB_URL}: {e}")
        print("The app will start, but database-dependent routes will not work.")
        client = None
        db = None


async def close_mongo_connection():
    """Close the MongoDB client connection."""
    global client, db
    if client is not None:
        client.close()
        print("Closed MongoDB connection.")
    client = None
    db = None


def get_database():
    """Return the database instance. May be None if MongoDB is unavailable."""
    return db