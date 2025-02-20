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
class EmailConfig:
    sender_email: str
    smtp_server: str
    smtp_port: int
    app_password: str
    tls: bool

    @classmethod
    def from_env(cls) -> "EmailConfig":
        return cls(
            sender_email=os.environ["EMAIL_SENDER"],
            smtp_server=os.environ["SMTP_SERVER"],
            smtp_port=int(os.environ["SMTP_PORT"]),
            app_password=os.environ["APP_PASSWORD"],
            tls=bool(os.environ["SMTP_TLS"]),
        )


@dataclass
class UrlConfig:
    base_url: str

    @classmethod
    def from_env(cls) -> "UrlConfig":
        return cls(base_url=os.environ["APP_BASE_URL"])


@dataclass
class RedisConfig:
    host: str
    port: int
    password: str

    @classmethod
    def from_env(cls) -> "RedisConfig":
        return cls(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ["REDIS_PORT"]),
            password=os.environ["REDIS_PASSWORD"],
        )


@dataclass
class Config:
    db: DbConfig
    email_config: EmailConfig
    url_config: UrlConfig
    redis_config: RedisConfig


def load_config() -> "Config":
    db = DbConfig.from_env()
    email_config = EmailConfig.from_env()
    url_config = UrlConfig.from_env()
    redis_config = RedisConfig.from_env()
    return Config(
        db=db,
        email_config=email_config,
        url_config=url_config,
        redis_config=redis_config,
    )
