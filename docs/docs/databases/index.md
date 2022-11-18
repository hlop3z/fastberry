!!! info "Alembic"

    The tool used to create migrations for SQL is [**Alembic**](https://pypi.org/project/alembic/) for **`SQLAlchemy`**.

```
python ./manage.py db {My-Command}
```

## Available **Commands**

| Command               | Description                                              |
| --------------------- | -------------------------------------------------------- |
| **`auto-migrate`**    | Database Make-Migrations & Migrate in a **single step**. |
| **`make-migrations`** | Database Make-Migrations.                                |
| **`migrate`**         | Database Migrate.                                        |
| **`upgrade`**         | Database Migrate (Upgrade).                              |
| **`downgrade`**       | Database Migrate (Downgrade).                            |
| **`history`**         | Database Migrations History.                             |
| **`reset`**           | Database Delete Migrations (All-Versions).               |
