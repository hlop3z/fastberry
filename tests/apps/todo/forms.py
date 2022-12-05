# -*- coding: utf-8 -*-
"""
    { Forms } for GraphQL
"""
import fastberry as fb

# Create Group "Form"
form = fb.input("form")

# Create your <forms> here.
@form
class Task:
    """Task's Client Input Form"""

    title = fb.value(str, default=None, required=True)
    description = fb.value(str, default=None, required=True)
    status = fb.value(str, default=None, required=True)
