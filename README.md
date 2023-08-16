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

Program runs in an infinite loop and does daily trading. To stop it, press ctrl+c. Stocks will manually have to be sold, and orders cancelled, via `python close_all_positions.py`

Please note that the program uses Alpaca API for trading, and thus requires valid API credentials. Replace `APCA_API_KEY_ID` and `APCA_API_SECRET_KEY` in the Python config.py file with your actual API key ID and secret key.

# Why I Built This Stock Trading Algorithm

The realm of algorithmic trading often seems like a labyrinth, melding together intricacies from diverse fields of knowledge. Whether it's coding, mathematics, finance, or strategy, every facet has its unique challenges. My ambition in creating this stock trading algorithm, utilizing the Alpaca API, was to strip away some of these complexities, rendering the process more accessible and understandable.

I envision a trading world where the technical and mathematical intricacies aren't barriers, but rather tools that everyone can harness. And in the pursuit of this vision, collaboration is key. I genuinely welcome inputs, insights, and contributions from the community. If you have ideas, refinements, or even critiques, I encourage you to submit a Pull Request. Together, we can refine this tool into an even more powerful learning tool for traders everywhere.


## Disclaimer

This software is for educational purposes only. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS. Do not risk money which you are afraid to lose. There might be bugs in the code - this software DOES NOT come with ANY warranty.


