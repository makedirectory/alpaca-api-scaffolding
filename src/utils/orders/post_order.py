import logging
from alpaca.trading.enums import OrderSide, TimeInForce
from src.api.alpaca.order_api import AlpacaOrderClient

# Logging setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PostAlpacaOrder:
    def __init__(self, trading_client):
        self.order_api = AlpacaOrderClient(trading_client)

    def post_market_order(self, symbol, trade_qty, side):
        logger.info(f"Placing {side} market order for {trade_qty} {symbol}.")

        if side is OrderSide.SELL and trade_qty == 0:
            logger.error(f"False start for {symbol}, stopping trade: {e}")
        
        try:
            # Define the order parameters
            symbol=symbol
            trade_qty = trade_qty
            side = side
            try:
                order = self.order_api.submit_market_order(symbol, trade_qty, side)
            except Exception as e:
                logger.error(f"Error placing order for {symbol}: {e}")
                return None

            # If order is successfully placed
            if side is OrderSide.BUY:
                pass
            elif side is OrderSide.SELL:
                pass
            return order
        except Exception as e:
            logger.error(f"Error placing order for {symbol}: {e}")
        return None
    
    def post_limit_order(self, symbol, trade_qty, side, limit_price):
        logger.info(f"Placing stop order for {trade_qty} {symbol} with limit price of: {limit_price}")
        
        try:
            # Define the order parameters
            symbol=symbol
            trade_qty = trade_qty
            side = side
            limit_price = limit_price
            order = self.order_api.submit_limit_order(symbol, trade_qty, side, limit_price)

            # If order is successfully placed
            if side is OrderSide.BUY:
                pass
            elif side is OrderSide.SELL:
                pass
            return order
        except Exception as e:
            logger.error(f"Error placing order for {symbol}: {e}")
        return None

    def post_stop_order(self, symbol, trade_qty, side, stop_price):
        logger.info(f"Placing stop order for {trade_qty} {symbol} with stop price of: {stop_price}")
        try:
            symbol=symbol
            trade_qty = trade_qty
            side = side
            stop_price = stop_price
            order = self.order_api.submit_stop_order(symbol, trade_qty, side, stop_price)

            # If order is successfully placed
            if side is OrderSide.BUY:
                pass
            elif side is OrderSide.SELL:
                pass
            return order
        except Exception as e:
            logger.error(f"Error placing stop order for {order.symbol}: {e}")
        return None
        
    def post_bracket_order(self, symbol, trade_qty, side, stop_price, take_profit):
        logger.info(f"Placing stop limit oco order: symbol: {symbol} qty: {trade_qty} take profit: {take_profit} stop: {stop_price}")

        try:
            symbol=symbol
            trade_qty=trade_qty
            side = side
            stop_price=stop_price # stop price
            take_profit=take_profit  # Trailing stop details
            order = self.order_api.submit_bracket_order(symbol, trade_qty, stop_price, take_profit)
            return order

        except Exception as e:
            logger.error(f"Error placing order for {symbol}: {e}")
        return None
