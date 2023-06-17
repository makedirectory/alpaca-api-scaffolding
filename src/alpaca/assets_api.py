from alpaca.trading.client import TradingClient
from alpaca.trading.enums import AssetClass
import logging
# Not sure if this is required. Included in documentation.
from alpaca.trading.requests import GetAssetsRequest

logger = logging.getLogger()

class AlpacaAssetsClient:
    def __init__(self, api_key, secret_key, base_url):
        self.client = TradingClient(api_key, secret_key, base_url)

    # TODO: How do we filter the equities we want to request?

    def get_all_equities(self):
        """Returns all US equities."""
        try:
            # search for US equities
            client = self.client
            search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
            assets = client.trading_client.get_all_assets(search_params)
            return assets
        except Exception as e:
            logger.error(f"Error fetching ALL us assets: {e}")
        return None
    

    def get_can_trade(self, symbol):
        """Can we trade this asset?"""
        try:
            # search for US equities
            client = self.client
            asset = client.get_asset(symbol)
            if asset.tradable:
                print(f'We can trade {asset}.')
            else:
                print(f'We can NOT trade {asset}.')
        except Exception as e:
            logger.error(f"Error determining if {asset} is tradable: {e}")
        return None