"""
from .mongo import Base as Mongo
from .sql import Base as Sql
import fastberry as fb

# Models Manager
model = fb.Model(sql=Sql, mongo=Mongo)
"""
