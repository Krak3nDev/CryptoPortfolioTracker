# test_data.py
from datetime import datetime, timezone

test_new_assets = [
    {
        "id": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "slug": "bitcoin",
        "cmc_rank": 1,
        "last_updated": "2024-08-23T18:32:00.000Z",
        "quote": {
            "USD": {
                "price": 63119.87,
                "volume_24h": 33719335646.03,
                "percent_change_1h": 2.07,
                "percent_change_24h": 4.36,
                "percent_change_7d": 6.24,
                "market_cap": 1246246282816.80,
                "last_updated": "2024-08-23T18:32:00.000Z",
            }
        },
    },
    {
        "id": 1027,
        "name": "Ethereum",
        "symbol": "ETH",
        "slug": "ethereum",
        "cmc_rank": 2,
        "last_updated": "2024-08-23T18:31:00.000Z",
        "quote": {
            "USD": {
                "price": 2722.36,
                "volume_24h": 14374200383.20,
                "percent_change_1h": 1.58,
                "percent_change_24h": 4.10,
                "percent_change_7d": 3.89,
                "market_cap": 327489044959.11,
                "last_updated": "2024-08-23T18:31:00.000Z",
            }
        },
    },
    {
        "id": 825,
        "name": "Tether",
        "symbol": "USDT",
        "slug": "tether",
        "cmc_rank": 3,
        "last_updated": "2024-08-23T18:30:00.000Z",
        "quote": {
            "USD": {
                "price": 1.00,
                "volume_24h": 49382479234.00,
                "percent_change_1h": 0.01,
                "percent_change_24h": 0.02,
                "percent_change_7d": 0.03,
                "market_cap": 68347123456.00,
                "last_updated": "2024-08-23T18:30:00.000Z",
            }
        },
    },
    {
        "id": 1831,
        "name": "Bitcoin Cash",
        "symbol": "BCH",
        "slug": "bitcoin-cash",
        "cmc_rank": 4,
        "last_updated": "2024-08-23T18:29:00.000Z",
        "quote": {
            "USD": {
                "price": 480.23,
                "volume_24h": 3214239856.12,
                "percent_change_1h": -0.56,
                "percent_change_24h": 1.12,
                "percent_change_7d": -2.34,
                "market_cap": 9023412345.67,
                "last_updated": "2024-08-23T18:29:00.000Z",
            }
        },
    },
]

test_existing_assets = [
    {
        "crypto_id": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "slug": "bitcoin",
        "cmc_rank": 1,
        "price": 62000.00,
        "percent_change_1h": 1.5,
        "percent_change_24h": 3.0,
        "percent_change_7d": 5.0,
        "last_updated": datetime(2024, 8, 20, 12, 30, tzinfo=timezone.utc),
    },
    {
        "crypto_id": 1027,
        "name": "Ethereum",
        "symbol": "ETH",
        "slug": "ethereum",
        "cmc_rank": 2,
        "price": 2700.00,
        "percent_change_1h": 1.0,
        "percent_change_24h": 2.0,
        "percent_change_7d": 3.0,
        "last_updated": datetime(2024, 8, 21, 12, 30, tzinfo=timezone.utc),
    },
    {
        "crypto_id": 825,
        "name": "Tether",
        "symbol": "USDT",
        "slug": "tether",
        "cmc_rank": 3,
        "price": 1.00,
        "percent_change_1h": 0.0,
        "percent_change_24h": 0.0,
        "percent_change_7d": 0.0,
        "last_updated": datetime(2024, 8, 22, 12, 30, tzinfo=timezone.utc),
    },
]

test_expected_assets_to_update = [
    {
        "crypto_id": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "slug": "bitcoin",
        "cmc_rank": 1,
        "price": 63119.87,
        "percent_change_1h": 2.07,
        "percent_change_24h": 4.36,
        "percent_change_7d": 6.24,
        "last_updated": datetime(2024, 8, 23, 18, 32, tzinfo=timezone.utc),
    },
    {
        "crypto_id": 1027,
        "name": "Ethereum",
        "symbol": "ETH",
        "slug": "ethereum",
        "cmc_rank": 2,
        "price": 2722.36,
        "percent_change_1h": 1.58,
        "percent_change_24h": 4.10,
        "percent_change_7d": 3.89,
        "last_updated": datetime(2024, 8, 23, 18, 31, tzinfo=timezone.utc),
    },
    {
        "crypto_id": 825,
        "name": "Tether",
        "symbol": "USDT",
        "slug": "tether",
        "cmc_rank": 3,
        "price": 1.00,
        "percent_change_1h": 0.01,
        "percent_change_24h": 0.02,
        "percent_change_7d": 0.03,
        "last_updated": datetime(2024, 8, 23, 18, 30, tzinfo=timezone.utc),
    },
    {
        "crypto_id": 1831,
        "name": "Bitcoin Cash",
        "symbol": "BCH",
        "slug": "bitcoin-cash",
        "cmc_rank": 4,
        "price": 480.23,
        "percent_change_1h": -0.56,
        "percent_change_24h": 1.12,
        "percent_change_7d": -2.34,
        "last_updated": datetime(2024, 8, 23, 18, 29, tzinfo=timezone.utc),
    },
]

test_assets_same_last_updated = [
    {
        "id": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "slug": "bitcoin",
        "cmc_rank": 1,
        "last_updated": "2024-08-23T18:32:00.000Z",
        "quote": {
            "USD": {
                "price": 63119.87,
                "percent_change_1h": 2.07,
                "percent_change_24h": 4.36,
                "percent_change_7d": 6.24,
                "last_updated": "2024-08-23T18:32:00.000Z",
            }
        },
    }
]

test_existing_assets_same_last_updated = [
    {
        "crypto_id": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "slug": "bitcoin",
        "cmc_rank": 1,
        "price": 63119.87,
        "percent_change_1h": 2.07,
        "percent_change_24h": 4.36,
        "percent_change_7d": 6.24,
        "last_updated": datetime(2024, 8, 23, 18, 32, tzinfo=timezone.utc),
    }
]

test_assets_older_new_data = [
    {
        "id": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "slug": "bitcoin",
        "cmc_rank": 1,
        "last_updated": "2024-08-23T18:30:00.000Z",
        "quote": {
            "USD": {
                "price": 63119.87,
                "percent_change_1h": 2.07,
                "percent_change_24h": 4.36,
                "percent_change_7d": 6.24,
                "last_updated": "2024-08-23T18:30:00.000Z",
            }
        },
    }
]

test_existing_assets_newer = [
    {
        "crypto_id": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "slug": "bitcoin",
        "cmc_rank": 1,
        "price": 63119.87,
        "percent_change_1h": 2.07,
        "percent_change_24h": 4.36,
        "percent_change_7d": 6.24,
        "last_updated": datetime(2024, 8, 23, 18, 32, tzinfo=timezone.utc),
    }
]
