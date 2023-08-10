import logging

from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass

logger = logging.getLogger()

class AlpacaAssetsClient:
    def __init__(self, trading_client):
        self.api = trading_client

    # TODO: How do we filter the equities we want to request?

    def get_all_equities(self):
        """Returns all US equities."""
        try:
            # search for US equities
            client = self.api
            search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
            assets = client.trading_client.get_all_assets(search_params)
            return assets
        except Exception as e:
            logger.error(f"Error fetching ALL us assets: {e}")
        return None
    

    def get_can_trade(self, symbol):
        """Can we trade this asset?"""

        if symbol is None:
            logger.error(f"Error determining if tradable. No symbol provided.")

        try:
            # search for US equities
            client = self.api
            asset = client.get_asset(symbol)
            return asset.tradable
        except Exception as e:
            logger.info(f"Error determining if {symbol} is tradable, removing from symbols: {e}")
        return None
