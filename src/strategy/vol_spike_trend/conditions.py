import logging
import asyncio
import traceback
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from alpaca.trading.enums import OrderSide, OrderType, PositionSide, OrderStatus
from alpaca.data.timeframe import TimeFrame

from src.utils.orders.post_order import PostAlpacaOrder
from src.portfolio_manager.position_allocator import PositionAllocator
from src.api.alpaca.data.historical_data import AlpacaHistData
from src.api.alpaca.assets_api import AlpacaAssetsClient
from src.api.alpaca.position_api import AlpacaPositionClient
from src.api.alpaca.order_api import AlpacaOrderClient
from src.indicators.rsi import RsiIndicator

# Logging setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OrderCondtions:
    def __init__(self, trading_client, asset_hist_client):
        self.position_allocator = PositionAllocator(trading_client, asset_hist_client)
        self.post_order = PostAlpacaOrder(trading_client)
        self.hist_api = AlpacaHistData(asset_hist_client)
        self.assets_api = AlpacaAssetsClient(trading_client)
        self.order_api = AlpacaOrderClient(trading_client)
        # Init strategy and Indicators
        self.open_positions = AlpacaPositionClient(trading_client)
        self.rsi = RsiIndicator()

    def volume_spike(self, df, volume_multiplier=1.5):
        average_volume = df['volume'].rolling(window=24).mean()
        df['volume_spike'] = df['volume'] > volume_multiplier * average_volume
        df['price_increase'] = df['close'] > df['close'].shift()
        df['RSI'] = self.rsi.RSI(series=df['close'], period=22)
        try:
            df['buy_signals'] = np.where((df['volume_spike'] == True) & (df['price_increase'] == True) & (df['RSI'] < 40), 1, 0)
            df['sell_signals'] = np.where((df['RSI'] > 70) | (df['RSI'] < 40), 1, 0)
            return df
        except Exception as e:
            logger.error("Could not generate signals.")

    async def check_trade_condition(self, symbol, trade_allocation, max_trade_allocation):

        can_trade = self.assets_api.get_can_trade(symbol)
        if can_trade is False:
            logger.info(f"Cannot trade {symbol}, skipping.")
            return

        # Get the current date
        now = datetime.now()
        start = now - timedelta(days=30,minutes=16)
        # Calculate the date - 1 day
        end = now - timedelta(minutes=16)
        timeframe = TimeFrame.Minute
        try:
            candles = self.hist_api.get_bars_for_ticker(symbol, start, end, timeframe)
        except Exception as e:
            logger.error(f"Error getting {symbol} ticker data: {e}")

        df = candles
        try:
            df_with_signals = self.volume_spike(df)
        except Exception as e:
            logger.error(f"error getting signals via vol spike.")

        try:
            buy_signal = df_with_signals['buy_signals'].iloc[-1]
            sell_signal = df_with_signals['sell_signals'].iloc[-1]
        except Exception as e:
            logger.error(f"Error getting signals for {symbol}.")

        try:
            # Get the lastest quote
            quote_data = self.hist_api.get_latest_quote(symbol)
            mean_price = (quote_data[symbol].ask_price + quote_data[symbol].bid_price) / 2
            current_price = mean_price
        except Exception as e:
            logger.error(f"Error getting quote data for {symbol}. Is the market open?")
            current_price = df['close'].iloc[-1]
            logger.error(f"It's okay, we got you. Using the last close instead.")

        if sell_signal:
            logger.info(f"Sell Signal triggered for {symbol}: checking position")
            try:
                current_position = self.open_positions.get_open_position(symbol)
            except Exception as e:
                logger.error(f"failed to get current position for {symbol}: {e}")
            
            if current_position is None:
                logger.info(f"Stopping sale of {symbol}. Non held")
                return
            
            try: 
                open_orders = self.order_api.list_open_orders(symbol, side=OrderSide.SELL)
                # if int(current_position.qty_available) != int(current_position.qty):
                # logger.info(f"Available qty and trading qty diverged for {symbol}")
                # Filter the list to find orders for the specified symbol
                symbol_orders = [order for order in open_orders if order.symbol == symbol]
                stop_orders = [order for order in symbol_orders if order.order_type == OrderType.STOP]
            except Exception as e:
                logger.error(f"failed to get open orders for {symbol}: {e}")
            # Canel open sell orders
            if stop_orders:
                logger.info(f"There are open sell orders for {symbol}. Must cancle them.")
                # Canceliing all orders
                # TODO: Handle other order types. ie: for order in stop_orders:
                for order in symbol_orders:
                    # print(f"symbol: {order.id}")
                    order_id = order.id
                    self.order_api.cancel_order(order_id)

            if current_position.side != PositionSide.LONG:
                logger.error(f"Stop Sell signal triggered for {symbol}, not long.")

            try:  
                logger.error(f"Sell signal triggered for {symbol}")
                sell_order = self.sell_order(symbol, current_position.qty)
                return sell_order
            except Exception as e:
                logger.info(f"failed to place sell order")


        if buy_signal:
            current_position = self.open_positions.get_open_position(symbol)
            open_orders = self.order_api.list_open_orders(symbol, side=OrderSide.BUY)

            # Filter the list to find orders for the specified symbol
            symbol_orders = [order for order in open_orders if order.symbol == symbol]

            if symbol_orders:
                logger.info(f"There are open buy orders for {symbol}. Not proceeding with trade...")
                return
            
            if int(current_position.qty) > 0:
                logger.info(f"Open positions for {symbol}. Not proceeding with trade...")
                return
            
            trade_qty = self.position_allocator.calculate_trade_size(symbol, trade_allocation, max_trade_allocation, current_price)

            if trade_qty == 0 or trade_qty is None:
                logger.error(f"Final Trade size is 0. Buy order failed")
                return
    
            try:
                logger.info(f"No open buy orders or positions for {symbol}. Proceeding with trade...")
                buy_order = self.buy_order(symbol, trade_qty)
                await asyncio.sleep(5)
            except Exception as e:
                logger.info("BUY ORDER FAILED")
                
            if buy_order is None:
                logger.error("buy order failed")
                return
            
            id = str(buy_order.id)
            logger.info(f"BUY ORDER {id} COMPLETE.")
            try: 
                position_stop_loss = self.position_allocator.get_stop_loss(symbol, current_price)
                # If under $1, round to .0001
                if position_stop_loss < 1.00:
                    stop = round(position_stop_loss, 4)
                # If over $1, round to .01
                if position_stop_loss >= 1.00:
                    stop = round(position_stop_loss, 2)

                # print(f"init_stop_price: {stop}")
                stop_price = float(stop)
                # print(f"stop_price: {stop_price}")

                max_loss = (current_price * trade_qty) - (stop_price * trade_qty)
                round_max_loss = round(max_loss, 4)
                logger.info(f"Max Position loss: {round_max_loss}")
            except Exception as e:
                logger.error(f"Error setting position stop loss for {symbol}: {e}")

            order_id = buy_order
            try:
                await self.manage_orders(symbol, trade_qty, stop_price, order_id)
                logger.info("STOP ORDER COMPLETE")
            except Exception as e:
                logger.info("STOP ORDER FAILED")
                

                


    # TODO: actively check for open orders without a stop loss
    # Main function to manage the orders
    async def manage_orders(self, symbol, trade_qty, stop_price, order_id):
        # Submit the original order
        original_order = order_id

        # Boolean flag to indicate if our original order has been filled
        order_filled = False

        while not order_filled:
            timeout = 10
            logger.info(f"Checking for filled order in {timeout} seconds...")
            await asyncio.sleep(timeout)  # wait a few seconds before checking again

            # check our recent orders to see if it's been filled
            recent_orders = self.order_api.list_open_orders(symbol, side=OrderSide.BUY, status='all', limit=10)
            for order in recent_orders:
                if order.id != original_order.id:
                    return
                if order.status != 'filled':
                    return
                logger.info(f"Checking status...")
                # our order was filled, let's place our stop loss order
                self.stop_loss_order(symbol, trade_qty, stop_price)
                order_filled = True  # exit the loop

    def buy_order(self, symbol, trade_qty):
        try:
            logger.info(f"Submit buy order for {trade_qty} of {symbol}.")
            side = OrderSide.BUY
            buy_order = self.post_order.post_market_order(symbol, trade_qty, side)
            if buy_order is None:
                logger.error("Buy order returned None.")

            if buy_order.status != OrderStatus.ACCEPTED or buy_order.status != OrderStatus.PENDING_NEW:
                logger.info(f"Buy Order submission failed for {symbol}.")

            logger.info(f"Buy Order placed successfully for {symbol}.")                
            return buy_order                
        except Exception as e:
            logger.error(f"Error placing buy order for {symbol}: {e}")
            # logger.error(traceback.format_exc())
        return None
    
    def stop_loss_order(self, symbol, trade_qty, stop_price): 
        try:
            logger.info(f"Submit stop loss for {trade_qty} of {symbol} at {stop_price}.")
            side = OrderSide.SELL
            stop_loss_order = self.post_order.post_stop_order(symbol, trade_qty, side, stop_price)
            if stop_loss_order is None:
               logger.error("Stop loss order returned None.")

            if stop_loss_order.status != OrderStatus.ACCEPTED or stop_loss_order.status != OrderStatus.PENDING_NEW:
                logger.info(f"Stop Order submission failed for {symbol}.")

            logger.info(f"Stop Order placed successfully for {symbol}.")
            return stop_loss_order
                
        except Exception as e:
            logger.error(f"Error placing buy order for {symbol}: {e}")
        return None

    def sell_order(self, symbol, current_position):
        try:
            logger.info(f"Submit sell order for {current_position} of {symbol}.")
            trade_qty = current_position
            side = OrderSide.SELL
            sell_order = self.post_order.post_market_order(symbol, trade_qty, side)
            if sell_order is None:
                logger.error("Sell order returned None.")
            if sell_order.status == OrderStatus.ACCEPTED or sell_order.status == OrderStatus.PENDING_NEW:
                logger.info(f"Sell Order submission failed for {symbol}.")

            logger.info(f"Sell Order placed successfully for {symbol}.")
            return sell_order                
        except Exception as e:
            logger.error(f"Error placing sell order for {current_position} {symbol}: {e}")
        return None