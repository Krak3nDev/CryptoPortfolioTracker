import asyncio
import logging
import os

import httpx
import pytest
import pytest_asyncio
from taskiq import InMemoryBroker

from cryptoapp.application.portfolio.create import BUCKET
from cryptoapp.infrastructure.persistence.tables.base import mapper_registry
from cryptoapp.main.config import (
    DbConfig,
    RabbitConfig,
    RedisConfig,
    S3MinioConfig,
    load_config,
)
from cryptoapp.main.di.setup import setup_ioc_container
from cryptoapp.main.taskiq_entry.broker import create_broker, configure_broker
from cryptoapp.main.web import create_app
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import AsyncEngine
from testcontainers.minio import MinioContainer
from testcontainers.postgres import PostgresContainer
from testcontainers.rabbitmq import RabbitMqContainer
from testcontainers.redis import RedisContainer


@pytest.fixture(scope="session")
def minio_container():
    minio_config = S3MinioConfig.from_env()

    with MinioContainer(
        "quay.io/minio/minio:RELEASE.2025-03-12T18-04-18Z",
        access_key=minio_config.aws_access_key,
        secret_key=minio_config.aws_secret_access_key,
        port=minio_config.port
    ) as minio:
        client = minio.get_client()
        client.make_bucket(BUCKET)
        yield minio


@pytest.fixture(scope="session")
def redis_container():
    redis_config = RedisConfig.from_env()

    with RedisContainer(
        "redis:latest", port=redis_config.port, password=redis_config.password
    ) as redis:
        yield redis


@pytest.fixture(scope="session")
def postgres_container():
    db_config = DbConfig.from_env()
    with PostgresContainer(
        image="postgres:16",
        username=db_config.user,
        password=db_config.password,
        dbname=db_config.database,
        driver="psycopg",
        port=db_config.port,
    ) as postgres:
        yield postgres


@pytest.fixture(scope="session")
def rabbitmq_container():
    rabbit_config = RabbitConfig.from_env()
    with RabbitMqContainer(
        image="rabbitmq:4.0",
        port=rabbit_config.port,
        username=rabbit_config.user,
        password=rabbit_config.password,
    ) as rabbit:
        yield rabbit


@pytest.fixture(scope="session")
def config(postgres_container, redis_container, minio_container):

    host = postgres_container.get_container_host_ip()
    port = postgres_container.get_exposed_port(int(os.environ["POSTGRES_PORT"]))

    redis_host = redis_container.get_container_host_ip()
    redis_port = redis_container.get_exposed_port(int(os.environ["REDIS_PORT"]))

    minio_host = minio_container.get_container_host_ip()
    minio_port = minio_container.get_exposed_port(int(os.environ["MINIO_PORT"]))

    os.environ["REDIS_HOST"] = redis_host
    os.environ["REDIS_PORT"] = str(redis_port)

    os.environ["POSTGRES_HOST"] = host
    os.environ["POSTGRES_PORT"] = str(port)
    os.environ["MINIO_HOST"] = minio_host
    os.environ["MINIO_PORT"] = str(minio_port)

    return load_config()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db_schema(container):
    engine = await container.get(
        AsyncEngine
    )
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

@pytest.fixture(scope="session")
def broker(config):
    broker = InMemoryBroker(await_inplace=True)
    configure_broker(config=config, broker=broker)
    return broker

@pytest.fixture(scope="session")
def container(config, broker):
    return setup_ioc_container(
        config=config,
        broker=broker
    )

@pytest.fixture(scope="session")
def app(container, broker):
    return create_app(container=container, broker=broker)

@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def scoped_container(container):
    async with container() as c:
        yield c

@pytest_asyncio.fixture(
    scope="session", loop_scope="session"
)
async def http_client(app):
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        yield client

@pytest.fixture(scope="session")
def email():
    return os.environ.get("EMAIL_LOGIN")