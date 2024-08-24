from dishka import make_async_container

from cryptoapp.main.depedencies.main_provider import MainProvider

provider = MainProvider()
container = make_async_container(provider)
