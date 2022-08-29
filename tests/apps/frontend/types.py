# -*- coding: utf-8 -*-
"""
    API - Strawberry Types
"""

# Create your <types> here.
import fastberry as fb

App = fb.Fastberry()
    
# print(App.types) 

# print("SQL: \n", App.controller.sql.get("default"), end="\n\n")
# print("Mongo: \n", App.controller.mongo.get("default"))

@fb.type
class Demo:
    category: list["Category"]
    author: list["Author"]

@App.mongo
class Author:
    name: str
    
@App.sql
class Product:
    # Core
    name: str
    stock: int = fb.default(1000000)
    is_available: bool = fb.default(False)
    
    # Date-Time
    created_at: fb.datetime = fb.default(fb.Date.datetime)
    available_from: fb.date = fb.default(fb.Date.date)
    same_day_shipping_before: fb.time = fb.default(fb.Date.time)
    
    # Decimal
    price: fb.decimal = fb.default(fb.decimal("100.20"))
    
    # Text
    message: fb.text = fb.default("Hello World")
    
    # List
    notes: list[fb.text] = fb.default(list)
    aliases: list[str] = fb.default(lambda: ["type", "class", "object"])
    
    # JSON (Dict or List)
    is_object: fb.json = fb.default(dict)
    is_json: fb.json = fb.default(lambda: { "message" : "Hello World" })

    # Via Functions
    async def demo(self) -> fb.ref["Demo"]:
        """
        print(App.models.sql.keys())
        print(App.models.mongo.keys())
        """
        category = App.models.sql.get("frontend.category")
        author = App.models.mongo.get("frontend.author")

        # await category.create({"name": "Awesome"})
        # await author.create({"name": "John Doe"})

        results_author = await author.all()
        results_category = await category.all()

        return Demo(
            author=results_author.data,
            category=results_category.data,
        )


@App.database.sql.model
class Category:
    name: str