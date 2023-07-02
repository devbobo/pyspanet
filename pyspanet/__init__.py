""" pyspanet module """
__version__ = "0.0.1"

from .client import SpaClient
from .config import SpaConfig
from .connection import SpaConnection
from .data import SpaData
from .exceptions import SpaConnectionError

try:
    import machine

    from .micro.client import SpaMicroClient
    from .micro.config import SpaMicroConfig
    from .micro.connection import SpaMicroConnection

    __all__ = [
        "SpaClient",
        "SpaConfig",
        "SpaConnection",
        "SpaData",
        "SpaConnectionError",
        "SpaMicroClient",
        "SpaMicroConfig",
        "SpaMicroConnection"
    ]
except ImportError:
    from .net.api import SpaNet
    from .net.client import SpaNetClient
    from .net.config import SpaNetConfig
    from .net.connection import SpaNetConnection

    __all__ = [
        "SpaClient",
        "SpaConfig",
        "SpaConnection",
        "SpaData",
        "SpaConnectionError",
        "SpaNet",
        "SpaNetClient",
        "SpaNetConfig",
        "SpaNetConnection"
    ]
