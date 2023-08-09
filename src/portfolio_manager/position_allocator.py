from scipy import stats
from src.api.alpaca.account_api import AlpacaAccountClient
from src.indicators.beta import BetaIndicator
import logging
import math

# Logging setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PositionAllocator:
    def __init__(self, trading_client, asset_hist_client):
        trading_client = trading_client
        self.account_api = AlpacaAccountClient(trading_client)
        # Compute the beta
        self.beta_indicator = BetaIndicator(asset_hist_client)
    
    def calculate_trade_size(self, symbol, trade_allocation, max_trade_allocation, current_price):
        # Set the trade size inversely proportional to the risk score

        if current_price is None or current_price == 0:
            logger.info("current_price is 0. Can not get trade size.")
            return
        try:
            account_capital = self.account_api.get_cash_balance()
            capital = float(account_capital)
            if capital < float(250.0):
                logger.info("Insufficient capital, no trades will be made.")
                return None
            

            trade_value = min(capital, trade_allocation)
            try:
                position_beta_score = self.get_position_beta(symbol)
            except Exception as e:
                 position_beta_score = 1.0
                 logger.error("failed to get position_beta_score")

            try:
                if position_beta_score == 0:
                    position_value = min(max_trade_allocation, trade_value)
                    trade_size = (position_value * 3) / current_price
                    trade_qty =  int(math.floor(trade_size))  # round to nearest integer before converting to int
                    return trade_qty
                elif 0 < position_beta_score <= 3:
                    position_value = trade_value / position_beta_score
                    final_position_value = min(max_trade_allocation, position_value)
                    trade_size = final_position_value / current_price
                    trade_qty =  int(math.floor(trade_size))  # round to lowest integer before converting to int
                    return trade_qty
                elif -3 <= position_beta_score < 0:
                    position_value = trade_value / abs(position_beta_score)
                    final_position_value = min(max_trade_allocation, position_value)
                    trade_size = final_position_value / current_price
                    trade_qty =  int(math.floor(trade_size))  # round to nearest integer before converting to int
                    return trade_qty
                else:
                    logger.info(f"invalid position beta in calculate_trade_size")
                    position_value = min(max_trade_allocation, trade_value)
                    trade_size = position_value / current_price
                    trade_qty =  int(math.floor(trade_size))  # round to nearest integer before converting to int
                    return trade_qty
            except Exception as e:
                logger.error(f"error getting final trade size: {e}")
            return None
        except Exception as e:
            logger.error(f"error getting position beta for trade size: {e}")
        return None
    
    def get_stop_loss(self, symbol, current_price, base_stop_loss=0.10):
        try:
            position_stop_loss = current_price - (current_price * base_stop_loss)
            return position_stop_loss
        except Exception as e:
                    logger.error(f"error getting position stop loss for {symbol}: {e}")
        return None
    
    def get_position_beta(self, symbol):
        try:

            beta_score = self.beta_indicator.compute_beta(symbol)
            # print(f"beta_score: {beta_score}")
            return beta_score
        except Exception as e:
                    logger.error(f"error getting position beta for {symbol}: {e}")
        return None