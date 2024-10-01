import logging
from alpaca.trading.enums import OrderSide
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
            order = self.order_api.submit_market_order(symbol, trade_qty, side)
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
        if trade_qty is None or limit_price is None:
            logger.error("no trade qty / take profit on Limit Order")


        logger.info(f"Placing stop order for {trade_qty} {symbol} with limit price of: {limit_price}")
        
        try:
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
        if trade_qty is None or stop_price is None:
            logger.error("no trade qty / stop price on Stop Order")
        logger.info(f"Placing stop order for {trade_qty} {symbol} with stop price of: {stop_price}")
        try:
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
        
    def post_bracket_order(self, symbol, side, trade_qty, stop_price, take_profit):
        if stop_price is None or take_profit is None:
            logger.error("no stop price / take profit on OCO Order")

        if side is None:
            logger.error("no side on OCO Order")


        logger.info(f"Placing stop limit oco order: symbol: {symbol} qty: {trade_qty} take profit: {take_profit} stop: {stop_price}")
        try:
            order = self.order_api.submit_bracket_order(symbol, side, trade_qty, stop_price, take_profit)
            return order

        except Exception as e:
            logger.error(f"Error placing order for {symbol}: {e}")
        return None
