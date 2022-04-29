"""
import motor.motor_asyncio

# Config
DATABASE_URL = "mongodb://localhost:27017"
DATABASE_NAME = "test_database"

# Engine
ENGINE = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)


# Base
Base = ENGINE[DATABASE_NAME]
"""
