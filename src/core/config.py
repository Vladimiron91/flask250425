from pathlib import Path
from typing import Any
from pydantic import SecretStr
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):
    # App settings
    app_name: str = "Community Pulse"
    debug: bool = True
    api_version: str = "v1"

    secret_key: SecretStr


    # DB settings
    mysql_host: str
    mysql_port: int = 3306
    mysql_user: str
    mysql_password: SecretStr
    mysql_database: str
    mysql_pool_size: int = 5
    mysql_pool_timeout: int = 30


    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        case_sensitive=False,
        extra='allow'
    )

    @property
    def database_url(self) -> str:
        # return "mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}".format(
        #     user=self.mysql_user,
        #     password=self.mysql_password.get_secret_value(),
        #     host=self.mysql_host,
        #     port=self.mysql_port,
        #     db_name=self.mysql_database
        # )
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        return f"sqlite:///{BASE_DIR}/db.sqlite3"

    def get_flask_config(self) -> dict[str, Any]:
        return {
            # "SECRET_KEY": self.secret_key,  #  -> *****************************
            "SECRET_KEY": self.secret_key.get_secret_value(),  #  my_secret_value
            "DEBUG": self.debug,
            "SQLALCHEMY_DATABASE_URI": self.database_url,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SQLALCHEMY_POOL_SIZE": self.mysql_pool_size,
            "SQLALCHEMY_POOL_TIMEOUT": self.mysql_pool_timeout
        }


settings = Settings()
