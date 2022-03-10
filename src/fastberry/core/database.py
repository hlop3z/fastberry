from .db import Mongo, Sql
from .imports import settings

try:
    DATABASES = settings.DATABASES
except:
    DATABASES = None

if DATABASES:
    # SETUP
    mongo_setup = DATABASES.get("MONGO", {})
    sql_setup = DATABASES.get("SQL", {})

    # URL
    mongo_url = mongo_setup.get("URL")
    sql_url = sql_setup.get("URL")

    # DATABASE-NAME
    mongo_db = mongo_setup.get("NAME")

    # MANAGERS
    sql = Sql(url=sql_url)
    mongo = Mongo(url=mongo_url, name=mongo_db)

else:
    # MANAGERS
    sql = None
    mongo = None
