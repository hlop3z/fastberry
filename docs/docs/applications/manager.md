> Your code **needs** to be in a **file** named **`manager.py`** or **folder** named **`manager`** inside your **Application**.

!!! info

    The purpose of the **manager** is to handle updates to the database

## File or Folder **Layout**

=== ":material-file: File"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- manager.py            --> <File> - Your code in HERE!
    |
    `-- etc...
    ```

=== ":material-folder: Folder"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- manager/            --> <Directory> - Your Manager(s) in HERE!
    |             |-- __init__.py     --> <File> - Your IMPORTS in HERE!
    |             `-- etc...
    |
    `-- etc...
    ```

!!! abstract "Tool"

    - **`fastberry.manager`**

## Python **Code**

=== ":material-file: File"

    ```python title="manager.py"
    # -*- coding: utf-8 -*-
    """
        { Controller } for the Database(s)
    """
    import fastberry as fb

    from . import types


    class Base:
        """Reusable Manager"""

        @classmethod
        async def all(cls):
            return await cls.objects.all()

        @classmethod
        async def reset_table(cls):
            return await cls.objects.delete(None, all=True)


    @fb.manager
    class Product(Base):
        """Product Manager"""

        model = types.Product

        @classmethod
        async def create(cls, form):
            results = None
            if form.is_valid:
                results = await cls.objects.create(form.data.__dict__)
            return results
    ```

=== ":material-folder: Folder"

    ```python title="__init__.py"
    # -*- coding: utf-8 -*-
    """
        Manager - Init
    """

    # Import your <managers> here.
    from .product import Product
    ```

    ``` python title="product.py"
    # -*- coding: utf-8 -*-
    """
        { Controller } for the Database(s)
    """

    import fastberry as fb

    from . import types


    class Base:
        """Reusable Manager"""

        @classmethod
        async def all(cls):
            return await cls.objects.all()

        @classmethod
        async def reset_table(cls):
            return await cls.objects.delete(None, all=True)


    @fb.manager
    class Product(Base):
        """Product Manager"""

        model = types.Product

        @classmethod
        async def create(cls, form):
            results = None
            if form.is_valid:
                results = await cls.objects.create(form.data.__dict__)
            return results
    ```
