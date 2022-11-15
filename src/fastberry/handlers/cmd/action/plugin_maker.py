""" [Plugin-Maker]
    Create Full-Plugin (Middleware, Extension, Permission, Router).
"""

MIDDLEWARE = '''
# -*- coding: utf-8 -*-
""" 
    [Middleware]
"""

from fastberry import BaseMiddleware

# Create <Middleware> here.

'''

EXTENSION = '''
# -*- coding: utf-8 -*-
""" 
    [Extension]
"""

from fastberry import BaseExtension

# Create <Extension> here.

'''

PERMISSION = '''
# -*- coding: utf-8 -*-
""" 
    [Permission]
"""

import typing

from strawberry.types import Info

from fastberry import BasePermission

# Create <Permission> here.

'''

ROUTER = '''
# -*- coding: utf-8 -*-
""" 
    [Router]
"""

from fastberry import Router

router = Router()

# Create <Router> here.

'''


def create_plugin(the_dir):
    """Create A Plugin"""

    with open(the_dir / "middleware.py", "w", encoding="utf-8") as file:
        file.write(MIDDLEWARE)

    with open(the_dir / "extension.py", "w", encoding="utf-8") as file:
        file.write(EXTENSION)

    with open(the_dir / "permission.py", "w", encoding="utf-8") as file:
        file.write(PERMISSION)

    with open(the_dir / "router.py", "w", encoding="utf-8") as file:
        file.write(ROUTER)
