from taskiq_aio_pika import AioPikaBroker

from cryptoapp.application.common.publisher import Publisher, SendActivationEmail
from cryptoapp.infrastructure.taskiq_tasks import send_mail_executor


class RabbitPublisher(Publisher):
    def __init__(self, rabbit: AioPikaBroker) -> None:
        self.rabbit = rabbit

    async def publish_email_task(self, event: SendActivationEmail) -> None:
        task = self.rabbit.task(task_name="send_mail")(send_mail_executor)
        await task.kiq(event)
