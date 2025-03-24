from httpx import (
    AsyncClient,
    RequestError,
    HTTPStatusError,
)
from tenacity import (
    wait_exponential,
    retry,
    stop_after_attempt,
    retry_if_exception_type,
)

from cryptoapp.infrastructure.services.marcetcap_api.schemas import (
    CryptoCurrency,
    CryptoCurrencyListingResponse,
)
from cryptoapp.main.config import CoinMarketCapConfig


class CoinMarketCapAPI:
    def __init__(
        self, client: AsyncClient, market_api_config: CoinMarketCapConfig
    ) -> None:
        self._client = client
        self._market_api_config = market_api_config

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((RequestError, HTTPStatusError)),
    )
    async def listing_cryptocurrencies(
        self, start: int = 1, limit: int = 5000
    ) -> list[CryptoCurrency]:
        response = await self._client.get(
            url=self._market_api_config.base_url + "/v1/cryptocurrency/listings/latest",
            headers={
                "X-CMC_PRO_API_KEY": self._market_api_config.token,
                "Accept": "application/json",
                "Accept-Encoding": "deflate, gzip",
            },
            params={"start": start, "limit": limit, "convert": "USD"},
        )
        response.raise_for_status()

        data: CryptoCurrencyListingResponse = response.json()

        return data["data"]


async def retrieve_all_data(
    api: CoinMarketCapAPI, start: int = 1, limit: int = 5000
) -> list[CryptoCurrency]:
    rows: list[CryptoCurrency] = []
    while True:
        data = await api.listing_cryptocurrencies(start=start, limit=limit)

        if len(data) < limit:
            break

        rows.extend(data)
        start += limit

    return rows


# async def main() -> None:
#     config = load_config()
#     engine = create_engine(db=config.db)
#
#     async with AsyncClient() as client:
#         api = CoinMarketCapAPI(client=client, market_api_config=config.coinmarketcap)
#         data = await retrieve_all_data(api)
#         assets = prepare_asset_rows(data)
#
#         async with AsyncSession(bind=engine) as session:
#             BATCH_SIZE = 2000
#             for chunk in batched(assets, BATCH_SIZE):
#                 await upsert_assets(data=chunk, session=session)
#

# if __name__ == "__main__":
#     asyncio.run(main())
