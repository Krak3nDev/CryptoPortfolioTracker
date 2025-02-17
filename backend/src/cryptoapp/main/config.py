import os
from dataclasses import dataclass

from sqlalchemy import URL


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    def construct_sqlalchemy_url(
        self,
        driver: str = "psycopg",
        host: str | None = None,
        port: int | None = None,
    ) -> str:
        # Если не указаны явно, берем host/port из объекта
        if not host:
            host = self.host
        if not port:
            port = self.port

        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)

    @classmethod
    def from_env(cls) -> "DbConfig":
        return cls(
            host=os.environ["POSTGRES_HOST"],
            password=os.environ["POSTGRES_PASSWORD"],
            user=os.environ["POSTGRES_USER"],
            database=os.environ["POSTGRES_DB"],
            port=int(os.environ["POSTGRES_PORT"]),
        )


@dataclass
class Config:
    db: DbConfig


def load_config() -> "Config":
    db = DbConfig.from_env()
    return Config(db=db)
