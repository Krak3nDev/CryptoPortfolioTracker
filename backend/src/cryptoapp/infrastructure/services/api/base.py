from __future__ import annotations

import asyncio
import logging
import ssl
from types import TracebackType
from typing import TYPE_CHECKING, Any, Optional, Type

import backoff
from aiohttp import ClientError, ClientSession, FormData, TCPConnector
from ujson import dumps, loads

if TYPE_CHECKING:
    from collections.abc import Mapping

    from yarl import URL


class BaseClient:
    def __init__(self, use_ssl: bool = True):
        self._session: ClientSession | None = None
        self.log = logging.getLogger(self.__class__.__name__)
        self.use_ssl = use_ssl

    async def _get_session(self) -> ClientSession:
        """Get aiohttp session with cache."""
        if self._session is None or self._session.closed:
            if self.use_ssl:
                ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ssl_context.load_default_certs()
                connector = TCPConnector(ssl_context=ssl_context)
            else:
                connector = None  # Use default connector which doesn't enforce SSL

            self._session = ClientSession(
                connector=connector,
                json_serialize=dumps,
            )

        return self._session

    @backoff.on_exception(backoff.expo, ClientError, max_time=60)
    async def _make_request(
        self,
        method: str,
        url: str | URL,
        params: Mapping[str, str] | None = None,
        json: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        data: FormData | None = None,
    ) -> tuple[int, dict[str, Any]]:
        session = await self._get_session()

        self.log.debug(
            "Making request %r %r with json %r and params %r",
            method,
            url,
            json,
            params,
        )
        async with session.request(
            method, url, params=params, json=json, headers=headers, data=data
        ) as response:
            status = response.status
            if status != 200:
                s = await response.text()
                raise ClientError(f"Got status {status} for {method} {url}: {s}")
            try:
                result = await response.json(loads=loads)
            except Exception as e:
                self.log.exception(e)
                self.log.info(f"{await response.text()}")
                result = {}

        self.log.debug(
            "Got response %r %r with status %r and json %r",
            method,
            url,
            status,
            result,
        )
        return status, result

    async def close(self) -> None:
        """Graceful session close."""
        if not self._session:
            self.log.debug("There's not session to close.")
            return

        if self._session.closed:
            self.log.debug("Session already closed.")
            return

        await self._session.close()
        self.log.debug("Session successfully closed.")

        # Adjust delay based on whether SSL is used
        await asyncio.sleep(0.250 if self.use_ssl else 0)

    async def __aenter__(self) -> BaseClient:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()
