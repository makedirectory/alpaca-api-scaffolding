from alpaca.trading.requests import (
    OrderRequest, LimitOrderRequest, MarketOrderRequest, StopOrderRequest, GetOrdersRequest, TakeProfitRequest, StopLossRequest
)
from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass, OrderType, QueryOrderStatus
import logging

logger = logging.getLogger()

class AlpacaOrderClient:
    def __init__(self, trading_client):
        self.trading_client = trading_client

    # TODO:
    # List orders open closed: https://alpaca.markets/docs/trading/getting_started/how-to-orders/#retrieve-all-orders
    # Submitting Bracket Orders: https://alpaca.markets/docs/trading/getting_started/how-to-orders/#submitting-bracket-orders
    # Submitting Trailing Stop Orders: https://alpaca.markets/docs/trading/getting_started/how-to-orders/#submitting-trailing-stop-orders
        

    def list_open_orders(self, symbol=None, side=None, status=QueryOrderStatus.OPEN, limit=500):
        """Returns a list of the account's orders by params."""
        try:
            request_params = GetOrdersRequest(
                symbol=symbol,
                side=side,  # Ex: OrderSide.SELL
                status=status,  # Ex: QueryOrderStatus.OPEN
                limit=limit
            )
            orders = self.trading_client.get_orders(filter=request_params)
            return orders
        except Exception as e:
            logger.error(f"Error listing orders: {e}")
        return None

    def cancel_all_orders(self):
        """Returns a list of the account's orders by params."""
        try:
            cancel_statuses = self.trading_client.cancel_orders()
            return cancel_statuses
        except Exception as e:
            logger.error(f"Error canceling all orders: {e}")
        return None
    
    def cancel_order(self, order_id):
        """Returns a list of the account's orders by params."""
        if order_id is None:
            logger.error(f"Error canceling order: order_id is None")
        try:
            cancel_status = self.trading_client.cancel_order_by_id(order_id)
            return cancel_status
        except Exception as e:
            logger.error(f"Error canceling order# {order_id}: {e}")
        return None

    def list_single_order(self, order_id):
        """Returns a list of the account's orders."""
        if order_id is None:
            logger.error(f"Error canceling order: order_id is None")
        try:
            order = self.trading_client.get_order_by_client_order_id(order_id)
            logger.info(f"Got order #{order_id}")
            return order
        except Exception as e:
            logger.error(f"Error getting order info for {order_id}: {e}")
        return None

    def submit_market_order(self, symbol, trade_qty, side):
        """Submits an order via the new SDK."""
        if symbol is None:
            logger.error(f"Empty Symbol on Market Order")
        if trade_qty is None:
            logger.error(f"Empty trade_qty on Market Order")
        if side is None:
            logger.error(f"Empty side on Market Order")

        try:
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                qty=trade_qty,
                side=side,
                time_in_force=TimeInForce.GTC
            )
            order = self.trading_client.submit_order(order_data=market_order_data)
            return order
        except Exception as e:
            logger.error(f"Error submitting order for {symbol}: {e}")
        return None

    def submit_limit_order(self, symbol, trade_qty, side, limit_price, notional=None):
        """Submits an order via the new SDK."""
        if symbol is None:
            logger.error(f"Empty Symbol on Limit Order")
        if trade_qty is None:
            logger.error(f"Empty trade_qty on Limit Order")
        if side is None:
            logger.error(f"Empty side on Limit Order")
        if limit_price is None:
            logger.error(f"Empty limit Price on Limit Order")

        try:
            limit_order_data = LimitOrderRequest(
                symbol=symbol,
                limit_price=limit_price,
                notional=notional,
                qty=trade_qty,
                side=side,
                time_in_force=TimeInForce.GTC  # TimeInForce.FOK
            )
            order = self.trading_client.submit_order(order_data=limit_order_data)
            return order
        except Exception as e:
            logger.error(f"Error submitting order for {symbol}: {e}")
        return None

    def submit_stop_order(self, symbol, trade_qty, side, stop_price, notional=None):
        """Submits an order via the new SDK."""
        if symbol is None:
            logger.error(f"Empty Symbol on Stop Order")
        if trade_qty is None:
            logger.error(f"Empty trade_qty on Stop Order")
        if side is None:
            logger.error(f"Empty side on Stop Order")
        if stop_price is None:
            logger.error(f"Empty Stop Price on Stop Order")

        try:
            stop_order_data = StopOrderRequest(
                symbol=symbol,
                stop_price=stop_price,
                notional=notional,
                qty=trade_qty,
                side=side,
                time_in_force=TimeInForce.GTC
            )
            order = self.trading_client.submit_order(order_data=stop_order_data)
            return order
        except Exception as e:
            logger.error(f"Error submitting order for {symbol}: {e}")
        return None
    
    def submit_bracket_order(self, symbol, trade_qty, side, take_profit, stop_loss):
        """Submits a bracket order via the new SDK."""
        if symbol is None:
            logger.error(f"Empty Symbol on Bracket Order")
        if trade_qty is None:
            logger.error(f"Empty Trade Qty on Bracket Order")
        if side is None:
            logger.error(f"Empty Side on Bracket Order")
        if take_profit is None:
            logger.error(f"Empty Take Profit on Bracket Order")
        if stop_loss is None:
            logger.error(f"Empty Stop Loss on Bracket Order")
        
        try:
            # Create the bracket order
            bracket_order_request = OrderRequest(
                symbol=symbol,
                qty=trade_qty,
                side=side,
                type=OrderType.MARKET,  # Market order
                time_in_force=TimeInForce.GTC,  # Good until cancelled
                order_class=OrderClass.BRACKET,  # Bracket order
                take_profit=TakeProfitRequest(limit_price=take_profit),  # Take profit details
                stop_loss=StopLossRequest(stop_price=stop_loss)  # Stop loss details
            )
            order = self.trading_client.submit_order(order_data=bracket_order_request)
            return order
        except Exception as e:
            logger.error(f"Error submitting bracket order for {symbol}: {e}")
        return None

    def submit_option_order(self, symbol, expiration_date, strike_price, option_type, qty, side):
        """Submits an option order."""
        if symbol is None or expiration_date is None or strike_price is None or option_type is None:
            logger.error("Missing required parameters for option order")
            return None

        try:
            option_symbol = f"{symbol}{expiration_date:%y%m%d}{option_type[0]}{int(strike_price):08d}"
            option_order_data = OrderRequest(
                symbol=option_symbol,
                qty=qty,
                side=side,
                type=OrderType.MARKET,
                time_in_force=TimeInForce.DAY
            )
            order = self.trading_client.submit_order(order_data=option_order_data)
            return order
        except Exception as e:
            logger.error(f"Error submitting option order for {symbol}: {e}")
        return None

    def submit_option_spread_order(self, symbol, expiration_date, legs):
        """Submits an option spread order."""
        if symbol is None or expiration_date is None or not legs:
            logger.error("Missing required parameters for option spread order")
            return None

        try:
            option_spread_order = OrderRequest(
                symbol=symbol,
                type=OrderType.MARKET,
                time_in_force=TimeInForce.DAY,
                order_class=OrderClass.OPTION_SPREAD,
                legs=legs
            )
            order = self.trading_client.submit_order(order_data=option_spread_order)
            return order
        except Exception as e:
            logger.error(f"Error submitting option spread order for {symbol}: {e}")
        return None

    def list_option_positions(self):
        """Lists all open option positions."""
        try:
            option_positions = self.trading_client.get_all_positions(asset_class='option')
            return option_positions
        except Exception as e:
            logger.error(f"Error fetching option positions: {e}")
        return None

    def close_option_position(self, symbol):
        """Closes an open option position."""
        if symbol is None:
            logger.error("Symbol is required to close an option position")
            return None

        try:
            close_position = self.trading_client.close_position(symbol)
            return close_position
        except Exception as e:
            logger.error(f"Error closing option position for {symbol}: {e}")
        return None

    def submit_trailing_stop_order(self, symbol, trade_qty, side, trail_price=None, trail_percent=None):
        """Submits a trailing stop order via the new SDK."""
        if symbol is None:
            logger.error(f"Empty Symbol on Trailing Stop Order")
        if trade_qty is None:
            logger.error(f"Empty Trade Qty on Trailing Stop Order")
        if side is None:
            logger.error(f"Empty Side on Trailing Stop Order")
        if trail_price is None and trail_percent is None:
            logger.error(f"Either trail_price or trail_percent must be provided on Trailing Stop Order")
        
        try:
            trailing_stop_order_data = StopOrderRequest(
                symbol=symbol,
                qty=trade_qty,
                side=side,
                time_in_force=TimeInForce.GTC,
                trail_price=trail_price,
                trail_percent=trail_percent
            )
            order = self.trading_client.submit_order(order_data=trailing_stop_order_data)
            return order
        except Exception as e:
            logger.error(f"Error submitting trailing stop order for {symbol}: {e}")
        return None
