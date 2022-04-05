"""
    BaseSettings created with Pydantic
"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Core Settings"""

    secret_key: str
    debug: bool = False
    mongo: str | None
    sql: str | None

    class Config:
        """Default Environmental File"""

        env_file = ".env"
