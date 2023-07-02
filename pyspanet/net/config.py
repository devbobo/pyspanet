""" SpaNetConfig class """
from __future__ import annotations

from dataclasses import dataclass
from ..config import SpaConfig

DEFAULT_PORT = 9090


@dataclass
class SpaNetConfig(SpaConfig):
    """SpaNet config"""
    def __init__(self, config: dict) -> None:
        self._host: str
        self._port: int
        self._mac_address: str
        self._member_id: int
        self._socket_id: int

        if 'id' in config:
            config['socket_id'] = config['id']

        if 'spaurl' in config:
            host, port = config['spaurl'].split(':', 1)
            config['host'] = host
            config['port'] = int(port)
        elif 'moburl' in config:
            host, port = config['moburl'].split(':', 1)
            config['host'] = host
            config['port'] = int(port)
        else:
            raise KeyError('missing "spaurl" and "moburl" from Config dict')

        self._host = config['host']
        self._port = config['port']

        if 'mac_address' in config:
            self._mac_address = config['mac_address']

        if 'id_member' in config:
            self._member_id = config['id_member']
        else:
            raise KeyError('missing "id_member" from Config dict')

        if 'name' in config:
            self._name = config['name']

        if 'id' in config:
            self._socket_id = config['id']
        elif 'id_sockets' in config:
            self._socket_id = config['id_sockets']
        else:
            raise KeyError('missing "id" and "socket_id" from Config dict')

        self._config = config

    @property
    def connect_string(self) -> str:
        """ connect_string: str"""
        return f'<connect--{self.socket_id}--{self.member_id}>'

    @property
    def host(self) -> str:
        """ host: str """
        return self._host

    @property
    def mac_address(self) -> str:
        """ mac_address: str"""
        return self._mac_address

    @property
    def member_id(self) -> int:
        """ member_id: int"""
        return self._member_id

    @property
    def socket_id(self) -> int:
        """ socket_id: int """
        return self._socket_id

    @property
    def port(self) -> int:
        """ port: int """
        return self._port | DEFAULT_PORT
