import logging
from alpaca.trading.enums import OrderSide, TimeInForce
from src.trade_executor import TradeExecutor
from src.portfolio_manager import PortfolioManager

# Logging setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Periods to look back for risk
RiskLookBackPeriod = 4
StopLoss = 10

class OrderCondtions:
    def __init__(self, api_key, api_secret, base_url, database_name):
        self.database_name = database_name
        self.order_strategy = TradeExecutor(api_key, api_secret, base_url)

    async def check_trade_condition(self, symbol, current_position):
        # If there is an existing position and indicators signal a bear market
        if self.bear_market:
            self.bear_market(symbol, current_position)
        # If there is no existing position and indicators signal a bull market
        elif self.bull_market:
            # TODO: Get position quantity
            self.bull_market(symbol)
            try: 
                # Set Stop Loss
                stop_price = symbol['close'] * (1 - StopLoss)
                # TODO: Get updated position quantity
                self.order_strategy.post_stop_order(symbol, stop_price, side=OrderSide.SELL, qty=1)
            except Exception as e:
                logger.error(f"Error setting stop loss order for {symbol}: {e}")
            return None

    def bull_market(self, symbol):
        try:
            # Pre-order tasks
            pass
            try:
                self.order_strategy.post_market_order(symbol, qty=1, side=OrderSide.BUY)  # modify quantity as needed
            except Exception as e:
                logger.error(f"Error placing buy order for {symbol}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error completing buy order for {symbol}: {e}")
        return None

    def bear_market(self, symbol, current_position):
        try:
            # Pre-order tasks
            pass
            try:
                self.order_strategy.post_market_order(symbol, qty=current_position.qty, side=OrderSide.SELL)
            except Exception as e:
                logger.error(f"Error placing sell order for {current_position.qty} {symbol}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error completing sell order for {current_position.qty} {symbol}: {e}")
        return None
    

    