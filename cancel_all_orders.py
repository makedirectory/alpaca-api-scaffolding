import logging
from src.api.alpaca.order_api import AlpacaOrderClient

# Logging setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OrderCondtions:
    def __init__(self, trading_client):
        self.order_api = AlpacaOrderClient(trading_client)

    def main(self):
        try:
            self.order_api.cancel_all_orders()
            logger.info("Orders Canceled")
        except Exception as e:
            logger.error(f"Failed to cancel all orders: {e}")

if __name__ == "__main__":
    from alpaca.trading.client import TradingClient
    import config
    trading_client = TradingClient(api_key=config.APCA_API_KEY_ID, secret_key=config.APCA_API_SECRET_KEY, paper=True)
    oc = OrderCondtions(trading_client)
    oc.main()