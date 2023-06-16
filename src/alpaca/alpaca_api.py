import alpaca_trade_api as tradeapi

class AlpacaAPI:
    def __init__(self, api_key, api_secret, base_url):
        self.api = tradeapi.REST(api_key, api_secret, base_url=base_url)