import logging
import pandas as pd
from datetime import datetime, timedelta

from alpaca.data.timeframe import TimeFrame
from src.api.alpaca.data.historical_data import AlpacaHistData 




# Logging setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BetaIndicator:
    def __init__(self, asset_hist_client):
        self.hist_api = AlpacaHistData(asset_hist_client)

    def compute_beta(self, symbol, benchmark='SPY'):
        # Define your start and end dates
        start = (datetime.now() - timedelta(days=90)).isoformat()  # Start date: 90 days ago
        end = (datetime.now() - timedelta(days=1)).isoformat()  # End date: one day ago

        # Fetch historical data for benchmark and symbol
        timeframe = TimeFrame.Minute
        benchmark_data = self.hist_api.get_bars_for_ticker(benchmark, start, end, timeframe)['close']
        symbol_data = self.hist_api.get_bars_for_ticker(symbol, start, end, timeframe)['close']

        # Reset index and set timestamp as index for both series
        benchmark_data = benchmark_data.reset_index(level=0, drop=True)
        symbol_data = symbol_data.reset_index(level=0, drop=True)

        # Create DataFrame with both series
        df = pd.concat([benchmark_data, symbol_data], axis=1)
        df.columns = [benchmark, symbol]

        # Calculate daily returns
        df['returns_' + symbol] = df[symbol].pct_change()
        df['returns_' + benchmark] = df[benchmark].pct_change()

        # Drop NA values
        df.dropna(inplace=True)

        # Calculate covariance and variance
        cov = df[['returns_' + symbol, 'returns_' + benchmark]].cov().iloc[0, 1]
        var = df['returns_' + benchmark].var()

        # Calculate beta
        beta = cov / var

        logger.info(f"beta: {beta}")

        return beta
