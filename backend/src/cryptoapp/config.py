from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from environs import Env
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
        driver: str = "asyncpg",
        host: Optional[str] = None,
        port: Optional[int] = 5439,
    ) -> str:
        # on localhost, port is 5439
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

    @staticmethod
    def from_env(env: Env) -> "DbConfig":
        """
        Creates the DbConfig object from environment variables.
        """
        host = env.str("DB_HOST")
        password = env.str("POSTGRES_PASSWORD")
        user = env.str("POSTGRES_USER")
        database = env.str("POSTGRES_DB")
        port = env.int("DB_PORT")
        return DbConfig(
            host=host, password=password, user=user, database=database, port=port
        )


@dataclass
class CoinMarketApiConfig:
    api_key: str
    base_url: str

    @staticmethod
    def from_env(env: Env) -> "CoinMarketApiConfig":
        api_key = env.str("COINMARKETCAP_API_KEY")
        base_url = env.str("BASE_URL")
        return CoinMarketApiConfig(api_key=api_key, base_url=base_url)


@dataclass
class AuthJWT:
    private_key_path: Path = Path("cryptoapp/certs/jwt-private.pem")
    public_key_path: Path = Path("cryptoapp/certs/jwt-public.pem")
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3


@dataclass
class EmailConfig:
    sender_email: str
    smtp_server: str
    smtp_port: int
    app_password: str
    tls: bool

    @staticmethod
    def from_env(env: Env) -> "EmailConfig":
        return EmailConfig(
            sender_email=env.str("EMAIL_SENDER"),
            smtp_server=env.str("SMTP_SERVER"),
            smtp_port=env.int("SMTP_PORT"),
            app_password=env.str("APP_PASSWORD"),
            tls=env.bool("SMTP_TLS"),
        )


@dataclass
class DomainConfig:
    domain: str

    @staticmethod
    def from_env(env: Env) -> "DomainConfig":
        domain = env.str("DOMAIN_URL")
        return DomainConfig(domain=domain)


@dataclass
class Config:
    db: DbConfig
    coin_market: CoinMarketApiConfig
    auth_jwt: AuthJWT
    email_data: EmailConfig
    domain: DomainConfig


def load_config(path: Optional[str] = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        db=DbConfig.from_env(env),
        coin_market=CoinMarketApiConfig.from_env(env),
        auth_jwt=AuthJWT(),
        email_data=EmailConfig.from_env(env),
        domain=DomainConfig.from_env(env),
    )
