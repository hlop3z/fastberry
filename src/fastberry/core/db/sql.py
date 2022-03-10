from types import SimpleNamespace

# SQL-Manager
from databases import Database

# SQL-Controller
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from dbcontroller import Sql

# Base
Base = declarative_base()


def init_sql(url: str = None):
    if url:
        # Setup
        engine = create_engine(url, echo=True)

        # Create-Tables
        def create_tables():
            Base.metadata.create_all(engine)
            return Base.metadata.tables

        database = Database(url)
        return SimpleNamespace(
            manager=Sql(database),
            base=Base,
            create_tables=create_tables,
            database=database,
        )
    return None
