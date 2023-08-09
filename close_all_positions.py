import argparse
import logging
from src.api.alpaca.position_api import AlpacaPositionClient

# Logging setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OrderCondtions:
    def __init__(self, trading_client):
        self.order_api = AlpacaPositionClient(trading_client)

    def main(self, cancel_orders=True):
        try:
            self.order_api.close_all_positions(cancel_orders)
            logger.info(f"positions closed")
        except Exception as e:
            logger.error(f"Failed to close all positions: {e}")

if __name__ == "__main__":
    from alpaca.trading.client import TradingClient
    import config

    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("--cancel_orders", default=True, type=bool,
                        help="Whether to cancel orders. Defaults to True.")
    args = parser.parse_args()

    trading_client = TradingClient(api_key=config.APCA_API_KEY_ID, secret_key=config.APCA_API_SECRET_KEY, paper=True)
    oc = OrderCondtions(trading_client)
    oc.main(args.cancel_orders)  # Pass cancel_orders argument from command line to main function
