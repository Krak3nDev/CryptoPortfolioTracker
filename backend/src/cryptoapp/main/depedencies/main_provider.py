from .application import ApplicationProvider
from .core import CoreProvider


class MainProvider(CoreProvider, ApplicationProvider): ...
