from decimal import Decimal, InvalidOperation
from typing import Iterable, Mapping, Any

from dateutil.parser import isoparse

from cryptoapp.infrastructure.services.marcetcap_api.schemas import CryptoCurrency
from cryptoapp.infrastructure.services.assets_updater.schemas import (
    AssetRow,
    TagExtractionResult,
    CmcIdToTagNames,
    AssetTagLink,
)


def extract_tags(
    data: Iterable[AssetRow], asset_id_map: Mapping[int, int]
) -> TagExtractionResult:
    cmc_id_to_tag_names: CmcIdToTagNames = {}
    all_tag_names = set()

    for currency in data:
        cmc_id = currency["cmc_id"]
        if cmc_id not in asset_id_map:
            continue

        tag_names = currency.get("tags", [])
        cmc_id_to_tag_names[cmc_id] = tag_names

        for tag_name in tag_names:
            all_tag_names.add(tag_name)

    return TagExtractionResult(
        cmc_id_to_tag_names=cmc_id_to_tag_names, all_tag_names=all_tag_names
    )


def build_assets_tags_rows(
    cmc_id_to_tag_names: CmcIdToTagNames,
    asset_id_map: Mapping[int, int],
    tag_id_map: dict[str, int],
) -> list[AssetTagLink]:
    assets_tags_rows = []
    for cmc_id, tag_names in cmc_id_to_tag_names.items():
        asset_id = asset_id_map[cmc_id]
        for tag_name in tag_names:
            if tag_name in tag_id_map:
                assets_tags_rows.append(
                    AssetTagLink(asset_id=asset_id, tag_id=tag_id_map[tag_name])
                )
    return assets_tags_rows


def safe_decimal(value: Any) -> Decimal:
    if value is None:
        return Decimal("0")
    try:
        d = Decimal(str(value))
        if not d.is_finite():
            return Decimal("0")
        return d
    except (InvalidOperation, TypeError):
        return Decimal("0")


def prepare_asset_rows(currencies: Iterable[CryptoCurrency]) -> list[AssetRow]:
    asset_rows = []
    for currency in currencies:
        quote_usd = currency["quote"]["USD"]

        date_added = isoparse(currency["date_added"])

        last_updated = isoparse(quote_usd["last_updated"])

        asset_rows.append(
            AssetRow(
                cmc_id=currency["id"],
                name=currency["name"],
                symbol=currency["symbol"],
                slug=currency["slug"],
                date_added=date_added,
                tags=currency.get("tags", []),
                is_infinite_supply=currency.get("infinite_supply", False),
                max_supply=safe_decimal(currency.get("max_supply")),
                total_supply=safe_decimal(currency.get("total_supply")),
                circulating_supply=safe_decimal(currency.get("circulating_supply")),
                price_usd=safe_decimal(quote_usd.get("price")),
                volume_24h_usd=safe_decimal(quote_usd.get("volume_24h")),
                market_cap_usd=safe_decimal(quote_usd.get("market_cap")),
                percent_change_1h_usd=safe_decimal(quote_usd.get("percent_change_1h")),
                percent_change_24h_usd=safe_decimal(
                    quote_usd.get("percent_change_24h")
                ),
                percent_change_7d_usd=safe_decimal(quote_usd.get("percent_change_7d")),
                last_updated=last_updated,
            )
        )
    return asset_rows
