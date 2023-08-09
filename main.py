import logging
import asyncio
from src.utils.trading_hours import TradingHours
from src.strategy.vol_spike_trend.run_strategy import Strategy
import config
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from datetime import timedelta
from src.api.alpaca.assets_api import AlpacaAssetsClient

# Logging Setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    
    # Instantiate Alpaca Trade Client
    trading_client = TradingClient(api_key=config.APCA_API_KEY_ID, secret_key=config.APCA_API_SECRET_KEY, paper=True)
    
    # Get market availability
    trading_hours = TradingHours(trading_client)

    # Cadence: Time to sleep after every full loop iteration, in seconds. 3 minutes in this case.
    cadence = 60 * 2

    # Symbols to trade
    symbols = ['NVDA', 'RIVN', 'NFLX', 'META', 'BAC', 
                 'MS', 'LM', 'TSLA', 'GS']
    assets_api = AlpacaAssetsClient(trading_client)
    # symbols = assets_api.get_all_equities()
    tradable_symbols = [symbol for symbol in symbols if assets_api.get_can_trade(symbol)]

    # Amount per trade
    max_trade_allocation = 1500.00
    trade_allocation = 500.00

    # Get Data 
    asset_hist_client = StockHistoricalDataClient(api_key=config.APCA_API_KEY_ID, secret_key=config.APCA_API_SECRET_KEY)
    # Init the Strategy
    strategy = Strategy(trading_client, asset_hist_client)

    # Define these functions outside the main loop
    async def market_open_tasks():
        # Rebalance portfolio at market open
        # TODO: Implement your function to rebalance portfolio here.
        logger.info("Algorithm is starting in 15 seconds...")
        await asyncio.sleep(15)

    async def market_close_tasks():
        # At market close calculate end-of-day statistics and pause algorithm
        # TODO: Implement function to calculate end-of-day statistics here.
        # Cancel any open buy orders at the end of the day.
        # orders = order_api.list_all_orders(status="open")
        # for order in orders:
        #     order_api.cancel_all_orders(order.id) # Update function to cancel one at a time
        minutes = int(cadence/60)
        logger.info(f"Market is closed. Algorithm is paused. Will check again in {minutes} minutes")

    async def run_strategies():
        # Run the trading strategy

        strategies = asyncio.gather(
            *[strategy.run_strategy(symbol, trade_allocation, max_trade_allocation) for symbol in tradable_symbols]
        )

        await strategies

    open_tasks_completed = False
    close_tasks_completed = False

    while True:
        current_time, is_market_open, next_open, next_close = trading_hours.get_market_status()

        if is_market_open:
            logger.info("Market is open.")

            if not open_tasks_completed and next_open + timedelta(minutes=3) >= current_time:
                await market_open_tasks()
                open_tasks_completed = True
                logger.info("Market open tasks complete. Trading begins...")
            
            await run_strategies()

            if not close_tasks_completed and next_close - timedelta(minutes=1) < current_time:
                await market_close_tasks()
                close_tasks_completed = True
        else:
            logger.info("Waiting for market to open...")
            open_tasks_completed = False
            close_tasks_completed = False

        # Sleep for the specified cadence time
        minutes = int(cadence/60)
        logger.info(f"Sleeping for {minutes} minutes before next iteration...")
        await asyncio.sleep(cadence)

if __name__ == "__main__":
    fmt = '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    fh = logging.FileHandler('console.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(fmt))
    logger.addHandler(fh)

    # Get the currently running event loop
    loop = asyncio.get_event_loop()

    # If there's no currently running event loop, create a new one
    if loop is None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        # Run the main coroutine until completion
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        # If we get a KeyboardInterrupt (e.g., from Ctrl+C), cancel all running tasks
        for task in asyncio.all_tasks(loop):
            task.cancel()
        # Now, gather all tasks. Because we've just cancelled them, this will give them a chance to 
        # clean up (i.e., execute any `finally` blocks) before they're destroyed.
        loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True))
    finally:
        # Close the loop
        loop.close()
