import pytest

from cryptoapp.infrastructure.database.mappers.assets import collect_assets_to_update
from ..test_data import test_new_assets, test_existing_assets, test_expected_assets_to_update, \
    test_assets_same_last_updated, test_assets_older_new_data, \
    test_existing_assets_newer, test_existing_assets_same_last_updated


@pytest.mark.parametrize("new_assets, existing_assets, expected_assets_to_update", [
    pytest.param(test_new_assets, test_existing_assets, test_expected_assets_to_update, id="update_all_assets"),
    pytest.param([], [], [], id="empty_assets"),
    pytest.param([test_new_assets[0]], [], [test_expected_assets_to_update[0]], id="add_single_new_asset"),
    pytest.param([], [test_existing_assets[0]], [], id="no_new_assets"),
    pytest.param(test_assets_same_last_updated, test_existing_assets_same_last_updated, [], id="same_last_updated"),
    pytest.param(test_assets_older_new_data, test_existing_assets_newer, [], id="older_new_data"),
])
def test_collect_assets_parametrized(new_assets, existing_assets, expected_assets_to_update):
    assets_to_update = collect_assets_to_update(new_assets, existing_assets)
    assert len(assets_to_update) == len(expected_assets_to_update)
    assert all(asset in assets_to_update for asset in expected_assets_to_update)
