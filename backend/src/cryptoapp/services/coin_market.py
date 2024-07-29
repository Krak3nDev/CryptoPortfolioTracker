from aiohttp.hdrs import METH_GET
from cryptoapp.services.base import BaseClient


class CoinMarketApi(BaseClient):
    def __init__(self, api_key: str, base_url: str):
        super().__init__()
        self.api_key = api_key
        self.base_url = base_url

    async def get_currencies(self):
        result = await self._make_request(
            method=METH_GET,
            url=self.base_url + "/cryptocurrency/listings/latest",
            headers={"X-CMC_PRO_API_KEY": self.api_key},
        )
        return result

    async def get_currency(self, currency_id: str):
        result = await self._make_request(
            method=METH_GET,
            url=self.base_url + "/cryptocurrency/quotes/latest",
            headers={"X-CMC_PRO_API_KEY": self.api_key},
            params={"id": currency_id},
        )
        return result


# async def main():
#     setup_logging()
#     config = load_config()
#     api = CoinMarketApi(api_key=config.coin_market.api_key,
#                         base_url=config.coin_market.base_url)
#
#     async with api:
#         result = await api.get_currencies(
#         )
#         print(
#             result
#         )
#
#
# asyncio.run(
#     main()
# )
