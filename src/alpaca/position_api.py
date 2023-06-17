from alpaca.trading.client import TradingClient
import logging

# Not sure if this is required. Included in documentation.
from alpaca.trading.requests import GetAssetsRequest

logger = logging.getLogger()

class AlpacaPositionClient:
    def __init__(self, api_key, secret_key, base_url):
        self.client = TradingClient(api_key, secret_key, base_url)

    def list_all_positions(self):
        """Returns a list of the account's active positions."""
        try:
            positions = self.client.get_all_positions()
            return positions
        except Exception as e:
            logger.error(f"Error fetching all positions: {e}")
        return None

    def get_open_position(self, symbol):
        """Returns the position for a specific symbol."""
        try:
            position = self.client.get_open_position(symbol)
            return position
        except Exception as e:
            logger.error(f"Error fetching open positions for {symbol}: {e}")
        return None

    def get_open_position_qty(self, symbol):
        try:
            position = self.get_open_position(symbol)
            quantity = position.qty
            return quantity
        except Exception as e:
            logger.error(f"Error fetching positions for {symbol}: {e}")
        return None

    def get_current_price(self, symbol):
        try:
            position = self.get_open_position(symbol)
            current_price = position.current_price
            return current_price
        except Exception as e:
            logger.error(f"Error fetching current price for {symbol}: {e}")
        return None
    
    def close_position(self, symbol):
        try:
            order = self.client.close_position(symbol)
            return order
        except Exception as e:
            logger.error(f"Error closing position for {symbol}: {e}")
        return None
    
    def close_all_positions(self, cancel_orders="false"):
        """Closes all account permissions and optionally cancels orders."""
        try:
            orders = self.client.close_all_positions(cancel_orders=cancel_orders)
            for order in orders:
                return order
        except Exception as e:
            logger.error(f"Error closing all positions: {e}")
        return None