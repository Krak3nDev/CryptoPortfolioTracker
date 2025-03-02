from dishka.integrations.fastapi import FastapiProvider

from .providers import (
    ActivationProvider,
    ConfigProvider,
    DbProvider,
    DomainServiceProvider,
    InfrastructureServiceProvider,
    InteractorProvider,
    MapperProvider,
)

providers = [
    InfrastructureServiceProvider(),
    DomainServiceProvider(),
    InteractorProvider(),
    MapperProvider(),
    DbProvider(),
    ConfigProvider(),
    ActivationProvider(),
    FastapiProvider(),
]
