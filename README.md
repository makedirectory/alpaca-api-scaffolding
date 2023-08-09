# Stock Trading Strategy Alpaca API

This project uses RSI, volume spikes, and upward direction of a given set of stocks, and executes a trading strategy based on these predictions using Alpaca API.

## Stocks 

The stocks used for trading can be changed in the `main.py` file. Update the symbols array with the tickers you want to trade.
```python
    # Symbols to trade
    symbols = ['NVDA', 'RIVN', 'NFLX', 'META']
```

## Portfolio

Risk is managed using beta and a hard trade limit. You can modify the trade ammount in the main.py file
```python
    # Amount per trade
    max_trade_allocation = 1500.00 // Trades will be capped at this amount
    trade_allocation = 500.00 // Trades start at this amount before taking beta into account
```

### Prerequisites

- Docker installed on your machine
- Alpaca API key and secret key
    - rename `config_example.py` to `config.py`

## How to Run

1. Clone this repository.

2. Navigate to the directory containing the files.

3. Build the Docker image:
    ```
    docker build -t trading-strategy .
    ```
4. Run the Docker container:
    ```
    docker run -it --rm trading-strategy
    ```

Please note that the program uses Alpaca API for trading, and thus requires valid API credentials. Replace `APCA_API_KEY_ID` and `APCA_API_SECRET_KEY` in the Python config.py file with your actual API key ID and secret key.