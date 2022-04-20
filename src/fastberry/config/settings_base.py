"""
    BaseSettings created with Pydantic
"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Core Settings"""

    secret_key: str
    debug: bool = False

    class Config:
        """Default Environmental File"""

        env_file = ".env"
