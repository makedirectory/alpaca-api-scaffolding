You can use these functions in your trading_bot.py file like this:

```python
from alpaca_api import AlpacaAccountClient

api = AlpacaAccountClient('<APCA-API-KEY-ID>', '<APCA-API-SECRET-KEY>')

# Get account details
account = api.get_account()
print(account)

# Get account balance
balance = api.get_cash_balance()
print(balance)
```

```python
from positions_api import AlpacaPositionClient

api = AlpacaPositionClient('<APCA-API-KEY-ID>', '<APCA-API-SECRET-KEY>')

# List positions
positions = api.list_all_positions()
print(positions)

# Get position for a specific symbol
position = api.get_open_position('AAPL')
print(position)
```

```python
from orders_api import AlpacaOrderClient
from alpaca.trading.enums import OrderSide, TimeInForce

api = AlpacaOrderClient('<APCA-API-KEY-ID>', '<APCA-API-SECRET-KEY>')

# List orders
orders = api.list_all_orders()
print(orders)

# Submit an order
order = api.submit_market_order(symbol='AAPL', qty=1, side=OrderSide.BUY, time_in_force=TimeInForce.GTC)
print(order)
```

```python
from data.historical_data import AlpacaHistData

api = AlpacaHistData('<APCA-API-KEY-ID>', '<APCA-API-SECRET-KEY>')

# List multiple symbols
symbol_data = api.get_hist_all_ticker_data(["NVDA", "AAPL", "MSFT"])
for symbol in symbol_data:
    print(symbol)

# List orders
candles = api.get_candle_for_all_ticker()
for candle in candles:
    print(candle)

```

Remember to replace '<APCA-API-KEY-ID>', '<APCA-API-SECRET-KEY>', 'https://paper-api.alpaca.markets' with your actual API key, secret key and the API endpoint.
