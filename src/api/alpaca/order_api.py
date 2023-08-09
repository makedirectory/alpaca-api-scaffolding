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
        

    def list_all_orders(self, symbol, side, status=QueryOrderStatus.OPEN, limit=500):
        """Returns a list of the account's orders by params."""
        try:
            request_params = GetOrdersRequest(
                symbol = symbol,
                side = side,  # Ex: OrderSide.SELL
                status = status,  # Ex: QueryOrderStatus.OPEN
                limit = limit
            )
            orders = self.trading_client.get_orders(filter=request_params)
            return orders
        except Exception as e:
            logger.error(f"Error listing orders for {symbol}: {e}")
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
    
    def submit_bracket_order(self, symbol, trade_qty, stop_price, take_profit):
        """Submits an order via the new SDK."""
        if symbol is None:
            logger.error(f"Empty Symbol on Stop Order")
        if trade_qty is None:
            logger.error(f"Empty Trade Qty on Stop Order")
        if take_profit is None:
            logger.error(f"Empty Take Profit on Stop Order")
        if stop_price is None:
            logger.error(f"Empty Stop Price on Stop Order")
        
        try:
            # Create the bracket order
            bracket_order_request = OrderRequest(
                symbol=symbol,
                qty=trade_qty,
                side=OrderSide.BUY,  # We're buying
                type=OrderType.MARKET,  # Market order
                time_in_force=TimeInForce.GTC,  # Good until cancelled
                order_class=OrderClass.BRACKET,  # Bracket order
                take_profit=TakeProfitRequest(limit_price=take_profit),  # Take profit details
                stop_loss=StopLossRequest(stop_price=stop_price)  # Stop loss details
            )
            order = self.trading_client.submit_order(order_data=bracket_order_request)
            return order
        except Exception as e:
            logger.error(f"Error submitting order for {symbol}: {e}")
        return None
