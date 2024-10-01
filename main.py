import logging
import asyncio
import config
import websockets
import json
import socket
from datetime import timedelta

from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient

from src.api.alpaca.calender import TradingCalendar
from src.strategy.vol_spike_trend.run_strategy import Strategy
from src.api.alpaca.assets_api import AlpacaAssetsClient

# Logging Setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def trading_paper():
    return config.PAPER_TRADE;

async def stream_account_actions():
    websocket = None  # Initialize websocket variable to None
    try:
        paper = await trading_paper()
        url = 'wss://paper-api.alpaca.markets/stream' if paper else 'wss://api.alpaca.markets/stream'
        async with websockets.connect(url) as websocket:
            await websocket.send(json.dumps({
                "action": "auth",
                "key": config.APCA_API_KEY_ID,
                "secret": config.APCA_API_SECRET_KEY
            }))
            response = await websocket.recv()
            logger.info(f"Account actions stream response: {response}")

            await websocket.send(json.dumps({
                "action": "listen",
                "data": {
                    "streams": ["trade_updates"]
                }
            }))
            while True:
                message = await websocket.recv()
                logger.info(f"Account action: {message}")
    except Exception as e:
        logger.error(f"An error occurred in stream_account_actions: {e}")
    
    finally:
        # Ensure WebSocket is closed if it was opened
        if websocket is not None:
            logger.info("Closing WebSocket connection for account actions.")
            await websocket.close()

async def stream_market_data(tickers):
    websocket = None  # Initialize websocket variable to None
    try:
        paper = await trading_paper()
        url = 'wss://paper-data.alpaca.markets/stream' if paper else 'wss://data.alpaca.markets/stream'
        async with websockets.connect(url) as websocket:
            await websocket.send(json.dumps({
                "action": "auth",
                "key": config.APCA_API_KEY_ID,
                "secret": config.APCA_API_SECRET_KEY
            }))
            response = await websocket.recv()
            logger.info(f"Market data stream response: {response}")

            await websocket.send(json.dumps({
                "action": "listen",
                "data": {
                    "streams": [f"T.{symbol}" for symbol in tickers]
                }
            }))
            while True:
                message = await websocket.recv()
                logger.info(f"Market data: {message}")
    except socket.gaierror as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if websocket is not None:
            logger.info("Closing WebSocket connection for market data.")
            await websocket.close()

async def main(tickers):
    # Instantiate Alpaca Trade Client
    paper = await trading_paper()
    trading_client = TradingClient(api_key=config.APCA_API_KEY_ID, secret_key=config.APCA_API_SECRET_KEY, paper=paper)
    
    # Get market availability
    trading_schedule = TradingCalendar(trading_client)

    # Cadence: Time to sleep after every full loop iteration, in seconds. 3 minutes in this case.
    cadence = 60 * 2
    
    assets_api = AlpacaAssetsClient(trading_client)
    # symbols = assets_api.get_all_equities()
    tradable_symbols = [ticker for ticker in tickers if assets_api.get_can_trade(ticker)]

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

    async def trading_tasks():
        # Run the trading strategy

        tasks = asyncio.gather(
            *[strategy.run_strategy(symbol, trade_allocation, max_trade_allocation) for symbol in tradable_symbols]
        )

        await tasks

    open_tasks_completed = False
    close_tasks_completed = False

    while True:
        market_status = trading_schedule.get_market_status()

        if market_status.is_market_open:
            logger.info("Market is open.")

            if not open_tasks_completed and market_status.next_open + timedelta(minutes=3) >= market_status.current_time:
                await market_open_tasks()
                open_tasks_completed = True
                logger.info("Market open tasks complete. Trading begins...")
            
            await trading_tasks()

            if not close_tasks_completed and market_status.next_close - timedelta(minutes=1) < market_status.current_time:
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

    # Symbols to trade
    tickers = ['NVDA', 'RIVN', 'NFLX', 'META', 'BAC', 
                 'MS', 'LM', 'TSLA', 'GS']

    # Get the currently running event loop
    loop = asyncio.get_event_loop()

    # If there's no currently running event loop, create a new one
    if loop is None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(asyncio.gather(
            main(tickers),
            stream_account_actions(),
            stream_market_data(tickers)
        ))
    except KeyboardInterrupt:
        # If we get a KeyboardInterrupt (e.g., from Ctrl+C), cancel all running tasks
        for task in asyncio.all_tasks(loop):
            task.cancel()
        # Now, gather all tasks. Because we've just cancelled them, this will give them a chance to 
        # clean up (i.e., execute any `finally` blocks) before they're destroyed.
        loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop), return_exceptions=True))
    except Exception as e:
        print(f"An error occurred in the main loop: {e}")
    finally:
        # Close the loop
        loop.close()