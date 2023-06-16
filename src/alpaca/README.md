You can use these functions in your trading_bot.py file like this:

```python
from alpaca_api import AlpacaAPI

api = AlpacaAPI('<APCA-API-KEY-ID>', '<APCA-API-SECRET-KEY>', 'https://paper-api.alpaca.markets')

# Get account details
account = api.get_account()
print(account)

# Get account balance
balance = api.get_balance()
print(balance)

# List positions
positions = api.list_positions()
for position in positions:
    print(position)

# Get position for a specific symbol
position = api.get_position('AAPL')
print(position)

# List orders
orders = api.list_orders()
for order in orders:
    print(order)

# Submit an order
order = api.submit_order(
    symbol='AAPL',
    qty=1,
    side='buy',
    type='market',
    time_in_force='gtc'
)
print(order)
```

Remember to replace '<APCA-API-KEY-ID>', '<APCA-API-SECRET-KEY>', 'https://paper-api.alpaca.markets' with your actual API key, secret key and the API endpoint.
