from datetime import datetime, date
import pytz
from dataclasses import dataclass
from alpaca.trading.requests import GetCalendarRequest

@dataclass
class MarketStatus:
    current_time: datetime
    is_market_open: bool
    next_open: datetime
    next_close: datetime

# Move this to api folder
class TradingCalendar:
    def __init__(self, trading_client):
        self.trading_client = trading_client
        self.calendar = self.load_calendar()

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
        return MarketStatus(current_time, is_market_open, next_open, next_close)

    def load_calendar(self):
        # Get today's date and set end date a few years into the future
        today = datetime.today().date()
        end_date = today.replace(year=today.year + 1)  # 1 year
        filters = GetCalendarRequest(
            start=today,
            end=end_date
        )
        calendar = self.trading_client.get_calendar(filters)
        if calendar:  # Check if the calendar list is not empty
            # print('Type of first item in calendar list:', type(calendar[0]))
            # print('First item in calendar list:', calendar[0])
            return calendar

    def is_first_trading_day_of_month(self):
        today = datetime.now(pytz.timezone('America/New_York')).date()
        # Find the earliest date in the calendar list for the current month and year
        first_trading_day = min(
            (
                day.date for day in self.calendar
                if day.date.month == today.month and day.date.year == today.year
            ),
            default=None
        )
        return first_trading_day == today

    def last_trading_day_of_month(self):
        today = datetime.now(pytz.timezone('America/New_York')).date()
        # Find the first day of the next month
        if today.month == 12:
            first_of_next_month = date(today.year + 1, 1, 1)
        else:
            first_of_next_month = date(today.year, today.month + 1, 1)

        # Iterate backwards through the calendar to find the last trading day of the current month
        last_trading_day = None
        for day in reversed(self.calendar):
            if day.date < first_of_next_month and day.date.month == today.month:
                last_trading_day = day.date
                break

        return last_trading_day
