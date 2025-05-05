from dishka import FromDishka
from dishka.integrations.taskiq import inject
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import AsyncBroker

from cryptoapp.application.common.publisher import SendActivationEmail
from cryptoapp.application.user.send_mail import EmailData, SendMailInteractor
from cryptoapp.infrastructure.services.assets_updater.sync import (
    update_all_assets,
)
from cryptoapp.infrastructure.services.marcetcap_api.api import (
    CoinMarketCapAPI,
)


@inject
async def send_mail_executor(
    data: SendActivationEmail, interactor: FromDishka[SendMailInteractor]
) -> None:
    await interactor(
        data=EmailData(email=data.email, username=data.username, url=data.url)
    )


@inject
async def update_assets(
    api: FromDishka[CoinMarketCapAPI], session: FromDishka[AsyncSession]
) -> None:
    await update_all_assets(api=api, session=session)


def register_tasks(broker: AsyncBroker) -> None:
    broker.register_task(send_mail_executor, task_name="send_mail")
    # broker.register_task(
    #     update_assets, task_name="update_assets",
    #     schedule=[{"cron": "*/10 * * * *"}]
    # )
