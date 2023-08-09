from datetime import datetime
import pytz

class TradingHours:
    def __init__(self, trading_client):
        self.trading_client = trading_client

    def get_market_calendar(self):
        date_today = datetime.now(pytz.timezone('America/New_York')).date()
        calendar = self.trading_client.get_calendar(date_today)
        return calendar
    
    def get_market_status(self):
        calendar = self.trading_client.get_clock()
        current_time = calendar.timestamp.astimezone(pytz.timezone('America/New_York'))
        next_open = calendar.next_open.astimezone(pytz.timezone('America/New_York'))
        next_close = calendar.next_close.astimezone(pytz.timezone('America/New_York'))
        is_market_open = calendar.is_open
        # For testing after hours
        # is_market_open = True
        return current_time, is_market_open, next_open, next_close