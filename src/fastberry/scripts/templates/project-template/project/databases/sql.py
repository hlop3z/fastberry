"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# Config
DATABASE_URL = "sqlite:///test_database.db"

# Engine
ENGINE = create_engine(DATABASE_URL, echo=True)


# Base
Base = declarative_base()
"""
