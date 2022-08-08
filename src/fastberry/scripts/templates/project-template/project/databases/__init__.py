"""
from .mongo import Base as Mongo
from .sql import Base as Sql

# Models Manager
model = fastberry.Model(sql=Sql, mongo=Mongo)
"""
