"""
    Database Manager (with dbcontroller)
    * https://pypi.org/project/dbcontroller/
"""

import pathlib

import motor.motor_asyncio
from databases import Database as DB
from dbcontroller import Mongo, Sql
from pymongo import MongoClient

from ..config import Settings
from ..utils.objects import Singleton


def mongo_url(path):
    """Process Mongo URL"""
    root = pathlib.Path(path)
    return dict(
        database=root.parts[-1:][0].split("?")[0], url="//".join(root.parts[:-1])
    )


class Database(Singleton):
    """Multi Database Manager"""

    def init(self):
        settings = Settings()

        def sql():
            database_url = settings.env.sql or "sqlite:///db.sqlite3"
            if database_url:
                database = DB(database_url)
                return Sql(database)
            return None

        def mongo_motor():
            mongo_env = settings.env.mongo
            if mongo_env:
                active = mongo_url(mongo_env)
                mongo_db = motor.motor_asyncio.AsyncIOMotorClient(
                    active.get("url", "mongodb://localhost:27017")
                )
                return Mongo(mongo_db)(active.get("database"))
            return None

        def mongo():
            mongo_env = settings.env.mongo
            if mongo_env:
                active = mongo_url(mongo_env)
                mongo_client = MongoClient(
                    active.get("url", "mongodb://localhost:27017")
                )
                return mongo_client[active.get("database")]
            return None

        # Start Values
        self.sql = sql()
        self.motor = mongo_motor()
        self.mongo = mongo()
