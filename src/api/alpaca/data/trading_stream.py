
class OrderTradingStream:
    def __init__(self, trade_stream):
        self.trading_stream = trade_stream

    async def update_handler(self, data):
        # trade updates will arrive in our async handler
        print(data)

    def run_trade_stream(self):
        # subscribe to trade updates and supply the handler as a parameter
        self.trading_stream.subscribe_trade_updates(self.update_handler)
        # start our websocket streaming
        self.trading_stream.run()
