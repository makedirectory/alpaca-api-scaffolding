import logging
from src.alpaca.alpaca_api import AlpacaAPI
from src.scanner.symbol_scanner import SymbolScanner
from src.portfolio_manager import PortfolioManager
from src.trade_executor import TradeExecutor

# Create a custom logger
logger = logging.getLogger(__name__)

# Set the level of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')

# Set level of handlers to DEBUG
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

class TradingBot:
    def __init__(self, api_key, api_secret, base_url):
        self.api = AlpacaAPI(api_key, api_secret, base_url)
        self.scanner = SymbolScanner(self.api)
        self.portfolio_manager = PortfolioManager(self.api)
        self.trade_executor = TradeExecutor(self.api)

    def run(self):
        while True:
            logger.info("Scanning symbols...")
            self.scanner.scan_symbols()
            logger.info("Managing portfolio...")
            self.portfolio_manager.manage_portfolio()
            logger.info("Executing trades...")
            self.trade_executor.execute_trades()

if __name__ == '__main__':
    bot = TradingBot('<APCA-API-KEY-ID>', '<APCA-API-SECRET-KEY>', 'https://paper-api.alpaca.markets')
    bot.run()
