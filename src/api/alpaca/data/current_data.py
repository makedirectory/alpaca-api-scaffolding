import logging
from alpaca.data import StockDataStream

logger = logging.getLogger()

class AlpacaCurrentDataStream:
    def __init__(self, symbol, api_client):
        self.symbol = symbol
        self.api_client = api_client
        self.wss_client = None

    async def quote_data_handler(self, data):
        # quote data will arrive here
        print(data)

    async def run_stream(self):
        self.wss_client = StockDataStream(self.api_client.api_key, self.api_client.secret_key)
        self.wss_client.subscribe_quotes(self.quote_data_handler, self.symbol)
        await self.wss_client.run()

# Example usage
# if __name__ == '__main__':
    # # api_client should be an object with api_key and secret_key attributes
    # stream = AlpacaCurrentDataStream('symbol', api_client)
    # asyncio.run(stream.run_stream())