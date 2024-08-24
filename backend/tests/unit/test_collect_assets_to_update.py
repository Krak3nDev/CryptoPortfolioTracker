import pytest

from cryptoapp.infrastructure.database.mappers.assets import collect_assets_to_update
from ..test_data import test_new_assets, test_existing_assets, test_expected_assets_to_update, \
    test_assets_same_last_updated, test_assets_older_new_data, \
    test_existing_assets_newer, test_existing_assets_same_last_updated


@pytest.mark.parametrize("new_assets, existing_assets, expected_assets_to_update", [
    (test_new_assets, test_existing_assets, test_expected_assets_to_update),
    ([], [], []),
    (
        [test_new_assets[0]],
        [],
        [test_expected_assets_to_update[0]]
    ),
    (
        [],
        [test_existing_assets[0]],
        []
    ),
    # Test: The same data, the update is not to blame
    (
        test_assets_same_last_updated,
        test_existing_assets_same_last_updated,
        []
    ),
    # Test: New data are old, updates are not to blame
    (
        test_assets_older_new_data,
        test_existing_assets_newer,
        []
    )
])
def test_collect_assets_parametrized(new_assets, existing_assets, expected_assets_to_update):
    assets_to_update = collect_assets_to_update(new_assets, existing_assets)
    assert len(assets_to_update) == len(expected_assets_to_update)
    assert all(asset in assets_to_update for asset in expected_assets_to_update)
