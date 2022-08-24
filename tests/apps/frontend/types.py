# -*- coding: utf-8 -*-
"""
    API - Strawberry Types
"""


import dataclasses as dc
import datetime
import decimal

import fastberry as fb

# Model
model = fb.Model()

@model.type
class Note:
    name: str
    text: fb.Text = dc.field(default_factory=list)


# Create Tables
# create_tables()
