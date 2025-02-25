from dishka import FromDishka
from dishka.integrations.taskiq import inject
from taskiq_aio_pika import AioPikaBroker

from cryptoapp.application.common.publisher import SendActivationEmail
from cryptoapp.application.user.send_mail import EmailData, SendMailInteractor


@inject  # type: ignore[misc]
async def send_mail_executor(
    data: SendActivationEmail, interactor: FromDishka[SendMailInteractor]
) -> None:
    await interactor(
        data=EmailData(email=data.email, username=data.username, url=data.url)
    )


def register_tasks(broker: AioPikaBroker) -> None:
    broker.register_task(send_mail_executor, task_name="send_mail")
