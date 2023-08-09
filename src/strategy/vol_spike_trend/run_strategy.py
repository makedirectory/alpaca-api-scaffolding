import logging
from src.strategy.vol_spike_trend.conditions import OrderCondtions
from src.strategy.strategy_base import StrategyBase

# Logging Setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Strategy(StrategyBase):
    def __init__(self, trading_client, asset_hist_client):
        # Order conditions. makes check to buy or sell
        self.order_conditions = OrderCondtions(trading_client, asset_hist_client)


    # TODO: Check predicted values the next day and run on strategy, if false flag, reverse order.
    async def run_strategy(self, symbol, trade_allocation, max_trade_allocation):

        await self.order_conditions.check_trade_condition(symbol, trade_allocation, max_trade_allocation)