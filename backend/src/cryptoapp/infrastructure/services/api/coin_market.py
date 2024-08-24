import asyncio
from typing import cast

import ujson
from aiohttp.hdrs import METH_GET

from cryptoapp.config import load_config
from cryptoapp.infrastructure.services.api.structures import CryptoResponse
from cryptoapp.utils.log import setup_logging
from .base import BaseClient


class CoinMarketApi(BaseClient):
    def __init__(self, api_key: str, base_url: str):
        super().__init__()
        self.api_key = api_key
        self.base_url = base_url

    async def get_assets(self) -> tuple[int, CryptoResponse]:
        result = await self._make_request(
            method=METH_GET,
            url=self.base_url + "cryptocurrency/listings/latest",
            headers={"X-CMC_PRO_API_KEY": self.api_key},
            params={"start": "1", "limit": "2"}
        )
        code, response_data = result
        crypto_response: CryptoResponse = cast(CryptoResponse, response_data)
        return code, crypto_response


async def main() -> None:
    setup_logging()
    config = load_config()
    print(config.coin_market.api_key)
    api = CoinMarketApi(api_key=config.coin_market.api_key,
                        base_url=config.coin_market.base_url)

    async with api:
        code, result = await api.get_assets(
        )
        formatted_json = ujson.dumps(result, indent=4, ensure_ascii=False)
        print(formatted_json)


if __name__ == "__main__":
    asyncio.run(main())
