# -*- coding: utf-8 -*-
"""
    API - Strawberry Types
"""

import dataclasses as dc
import datetime
import decimal
import typing

# Create your <types> here.
from fastberry import JSON, Model, Text

model = Model()

@model.type
class Author:
    name: str

@model.type
class Product:
    """
    query MyQuery {
        demoDetail {
            name
            aliases
            stock
            isAvailable
            createdAt
            sameDayShippingBefore
            price
            notes
            isObject
            category {
                name
            }
        }
    }
    """
    name: str
    aliases: list[str] | None = None
    stock: int | None = None
    is_available: bool | None = None
    available_from: datetime.date | None = None
    created_at: datetime.datetime | None = None
    same_day_shipping_before: datetime.time | None = None
    price: decimal.Decimal | None = None
    notes: list[Text] = dc.field(default_factory=list)
    is_object: JSON = dc.field(default_factory=dict)

    async def category(self) -> typing.Optional["Category"]:
        return Category(name="awesome")


@model.type
class Category:
    name: str
