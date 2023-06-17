from alpaca.trading.client import TradingClient
from alpaca.trading.requests import LimitOrderRequest, MarketOrderRequest, StopOrderRequest, GetOrdersRequest
# from alpaca.trading.enums import OrderSide, QueryOrderStatus
import logging

logger = logging.getLogger()

class AlpacaOrderClient:
    def __init__(self, api_key, secret_key, base_url):
        self.client = TradingClient(api_key, secret_key, base_url)

    def list_all_orders(self, status, side):
        """Returns a list of the account's orders by params."""
        try:
            # params to filter orders by
            request_params = GetOrdersRequest(
                status=status, # Ex: QueryOrderStatus.OPEN
                side=side # Ex: OrderSide.SELL
                )
            # orders that satisfy params
            orders = self.client.get_orders(filter=request_params)
            return orders
        except Exception as e:
            logger.error(f"Error listing all orders for {side} {status}: {e}")
        return None
    
    # TODO: List orders open closed: https://alpaca.markets/docs/trading/getting_started/how-to-orders/#retrieve-all-orders
    
    def cancel_all_orders(self):
        """Returns a list of the account's orders by params."""
        try:
            cancel_statuses = self.client.cancel_orders()
            return cancel_statuses
        except Exception as e:
            logger.error(f"Error canceling all orders: {e}")
        return None
    
    def list_single_order(self, order_id):
        """Returns a list of the account's orders."""
        try:
            my_order = self.client.get_order_by_client_order_id(order_id)
            return print(f'Got order #{my_order.id}')
        except Exception as e:
            logger.error(f"Error getting order info for {order_id}: {e}")
        return None

    def submit_market_order(self, symbol, qty, side, time_in_force):
        """Submits an order via the new SDK."""
        try:
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=side,
                time_in_force=time_in_force
                )
            self.order = self.client.submit_order(order_data=market_order_data)
            return self.order
        except Exception as e:
            logger.error(f"Error submitting order for {symbol}: {e}")
        return None

    def submit_limit_order(self, symbol, side, time_in_force, limit_price, notional=None, qty=None):
        """Submits an order via the new SDK."""
        try:
            limit_order_data = LimitOrderRequest(
                symbol=symbol,
                limit_price=limit_price,
                notional=notional,
                qty=qty,
                side=side,
                time_in_force=time_in_force # TimeInForce.FOK
                )
            self.order = self.client.submit_order(order_data=limit_order_data)
            return self.order
        except Exception as e:
            logger.error(f"Error submitting order for {symbol}: {e}")
        return None
        
    def submit_stop_order(self, symbol, side, time_in_force, stop_price, notional=None, qty=None):
        """Submits an order via the new SDK."""
        try:
            stop_limit_order_data = StopOrderRequest(
                symbol=symbol,
                stop_price=stop_price,
                notional=notional,
                qty=qty,
                side=side,
                time_in_force=time_in_force
                )
            self.order = self.client.submit_order(order_data=stop_limit_order_data)
            return self.order
        except Exception as e:
            logger.error(f"Error submitting order for {symbol}: {e}")
        return None
    

    # TODO: Submitting Bracket Orders: https://alpaca.markets/docs/trading/getting_started/how-to-orders/#submitting-bracket-orders
    # TODO: Submitting Trailing Stop Orders: https://alpaca.markets/docs/trading/getting_started/how-to-orders/#submitting-trailing-stop-orders
        
