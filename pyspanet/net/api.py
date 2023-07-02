""" SpaNet class """
from __future__ import annotations

import base64
import hmac
import json
from typing import Any

import aiohttp

from .config import SpaNetConfig

API_KEY = '4a483b9a-8f02-4e46-8bfa-0cf5732dbbd5'
API_URL = 'https://api.spanet.net.au/api'

LOGIN_URL = f'{API_URL}/MemberLogin'
SOCKETS_URL = f'{API_URL}/membersockets'

SPANET_SECRET = b'1ld0gVand'


class SpaNet():
    """ SpaNet """
    def __init__(self, username: str, password: str) -> None:
        self._username = username
        self._password = password

        self._member_id: int
        self._session_id: str

    @property
    def hashed_password(self) -> str:
        """ hashed_password: str """
        _hash = hmac.digest(
            SPANET_SECRET,
            bytes(self._password, 'utf-8'),
            'sha256'
        )
        return base64.b64encode(_hash) \
            .replace(b'+', b'1') \
            .replace(b'/', b'2') \
            .replace(b'=', b'3') \
            .decode()

    async def login(self) -> bool:
        """Login to SpaNet"""
        data = {
            'api_key': API_KEY,
            'login': self._username,
            'password': self.hashed_password
        }

        async with aiohttp.request(
            'POST',
            LOGIN_URL,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'},
        ) as response:
            if response.status != 200:
                return False

            result = await response.json()

            if 'success' not in result or not result['success']:
                return False

            if 'data' not in result:
                return False

            self._session_id = result['data']['id_session']
            self._member_id = result['data']['id_member']

            return True

    async def get_sockets(self) -> list:
        """ get_sockets """
        url = SOCKETS_URL
        member = self._member_id
        session = self._session_id

        async with aiohttp.request(
            'GET',
            f'{url}?id_member={member}&id_session={session}'
        ) as response:
            if response.status != 200:
                raise Exception()

            result = await response.json()

            if 'success' not in result or not result['success']:
                raise KeyError()

            if 'sockets' not in result:
                raise KeyError()

            sockets = []

            for socket in result['sockets']:
                sockets.append(SpaNetConfig(socket))

            return sockets

    async def __aenter__(self) -> SpaNet:
        """Connect and start listening for messages."""
        if not await self.login():
            raise Exception()
        return self

    async def __aexit__(self, *exctype: Any) -> None:
        """Disconnect."""
