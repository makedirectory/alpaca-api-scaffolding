import logging
import asyncio
import config
from datetime import timedelta
from app import main, stream_account_actions, stream_market_data

# Logging Setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    fmt = '%(asctime)s:%(filename)s:%(lineno)d:%(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    fh = logging.FileHandler('console.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(fmt))
    logger.addHandler(fh)

    # socketio.run(app, debug=True, host='0.0.0.0', port=5000)

    # Symbols to trade
    tickers = ['NVDA', 'RIVN', 'NFLX', 'META', 'BAC', 
                 'MS', 'LM', 'TSLA', 'GS', 'MSFT']

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
        # Handle KeyboardInterrupt and cancel all tasks
        logger.info("KeyboardInterrupt received. Canceling tasks...")
        tasks = asyncio.all_tasks(loop)
        for task in tasks:
            task.cancel()
        # Wait for all tasks to be cancelled properly
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
    except Exception as e:
        logger.error(f"An error occurred in the main loop: {e}")
    finally:
        # Ensure the event loop is properly closed
        logger.info("Closing the event loop.")
        loop.close()