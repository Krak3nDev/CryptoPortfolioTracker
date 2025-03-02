from aio_pika import ExchangeType
from dishka.integrations.taskiq import setup_dishka
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

from cryptoapp.main.config import Config, load_config
from cryptoapp.main.di.setup import setup_ioc_container
from cryptoapp.presentation.task_executor.tasks import register_tasks


def create_broker(config: Config) -> AioPikaBroker:
    broker = AioPikaBroker(
        url=config.rabbit_config.amqp_url,
        exchange_type=ExchangeType.DIRECT,
        declare_exchange=True,
        routing_key="send_mail",
        declare_queues_kwargs={"durable": True},
        declare_exchange_kwargs={"durable": True},
    ).with_result_backend(RedisAsyncResultBackend(redis_url=config.redis_config.url))

    register_tasks(broker)

    return broker


config = load_config()
broker = create_broker(config)
container = setup_ioc_container(config=config, broker=broker)
setup_dishka(container=container, broker=broker)
