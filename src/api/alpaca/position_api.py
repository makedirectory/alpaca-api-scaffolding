import logging

logger = logging.getLogger()

class AlpacaPositionClient:
    def __init__(self, trading_client):
        self.trading_client = trading_client

    def list_all_positions(self):
        """Returns a list of the account's active positions."""
        try:
            positions = self.trading_client.get_all_positions()
            return positions
        except Exception as e:
            logger.error(f"Error fetching all positions: {e}")
        return None

    def get_open_position(self, symbol):
        """Returns the position for a specific symbol."""

        if symbol is None:
            logger.error(f"Error getting open position. No symbol provided.")
        try:
            position = self.trading_client.get_open_position(symbol)
            return position
        except Exception as e:
            logger.info(f"No open positions for {symbol}: {e}")
        return None

    def get_open_position_qty(self, symbol):
        if symbol is None:
            logger.error(f"Error getting open position qty. No symbol provided.")
        try:
            position = self.get_open_position(symbol)
            quantity = position.qty
            return quantity
        except Exception as e:
            logger.info(f"Error fetching positions for {symbol}: {e}")
        return None

    def get_current_price(self, symbol):
        if symbol is None:
            logger.error(f"Error getting open position price. No symbol provided.")
        try:
            position = self.get_open_position(symbol)
            current_price = position.current_price
            return current_price
        except Exception as e:
            logger.info(f"Error fetching current price for {symbol}: {e}")
        return None

    def close_position(self, symbol):
        if symbol is None:
            logger.error(f"Error closing position. No symbol provided.")
        try:
            order = self.trading_client.close_position(symbol)
            return order
        except Exception as e:
            logger.info(f"Error closing position for {symbol}: {e}")
        return None

    def close_all_positions(self, cancel_orders="false"):
        """Closes all account permissions and optionally cancels orders."""
        try:
            orders = self.trading_client.close_all_positions(cancel_orders=cancel_orders)
            for order in orders:
                return order
        except Exception as e:
            logger.info(f"Error closing all positions: {e}")
        return None
