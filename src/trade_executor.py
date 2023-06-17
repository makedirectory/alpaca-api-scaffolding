import logging
from alpaca.trading.enums import OrderSide, TimeInForce
from src.alpaca.order_api import AlpacaOrderClient

# Logging setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TradeExecutor:
    def __init__(self, api):
        self.api = api
        self.order_client = AlpacaOrderClient(self.api)

    def post_market_order(self, symbol, qty, side, time_in_force=TimeInForce.GTC):
        logger.info(f"Placing order: {symbol} {qty}")
        
        try:
            # Define the order parameters
            side = side
            time_in_force = time_in_force
            order = self.order_client.submit_market_order(symbol, qty, side, time_in_force)

            # If order is successfully placed, update the database
            if side is OrderSide.BUY:
                # TODO:
                pass
            elif side is OrderSide.SELL:
                # TODO:
                pass
            return order
        except Exception as e:
            logger.error(f"Error placing order for {symbol}: {e}")
        return None

    def post_stop_order(self, symbol, qty, side, stop_price, time_in_force=TimeInForce.GTC):
        logger.info(f"Placing stop order: {symbol} {qty} at {stop_price}")
        # TODO: Check if stock exists in active list
        try:
            side=side
            time_in_force=time_in_force
            order = self.order_client.submit_stop_order(symbol, qty, side, stop_price, time_in_force)

            # If order is successfully placed, update the database
            if side is OrderSide.BUY:
                # TODO:
                pass
            elif side is OrderSide.SELL:
                # TODO:
                pass
            return order
        except Exception as e:
            logger.error(f"Error placing stop order for {order.symbol}: {e}")
        return None
    

    def post_limit_order(self, symbol, side, qty, limit_price, time_in_force=TimeInForce.GTC):
        logger.info(f"Placing order: {symbol} {qty}")
        
        try:
            # Define the order parameters
            side = side
            time_in_force = time_in_force
            limit_price = limit_price
            order = self.order_client.submit_limit_order(symbol, qty, side, limit_price, time_in_force)

            # If order is successfully placed, update the database
            if side is OrderSide.BUY:
                # TODO:
                pass
            elif side is OrderSide.SELL:
                # TODO:
                pass
            return order
        except Exception as e:
            logger.error(f"Error placing order for {symbol}: {e}")
        return None
