from types import SimpleNamespace

# Mongo-Controller
import motor.motor_asyncio

# Mongo-Manager
from dbcontroller import Mongo


def init_mongo(url: str = None, name: str = None):
    if url and name:
        # Setup
        MONGO_DB = motor.motor_asyncio.AsyncIOMotorClient(url)
        # Mongo
        MONGO_DB[name]
        return SimpleNamespace(manager=Mongo(MONGO_DB)(name), base=MONGO_DB[name])
    return None
