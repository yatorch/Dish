# Utility funcs

import datetime as dt
import pandas_market_calendars as mcal
import pandas as pd


def get_latest_mclose_date():
    nasdaq_calendar = mcal.get_calendar('NASDAQ')
    date_today_raw = dt.date.today()
    start_date_nd = date_today_raw - dt.timedelta(days=7)
    nasdaq_schedule = nasdaq_calendar.schedule(start_date=start_date_nd, end_date=date_today_raw)
    print(f"last market close: {nasdaq_schedule['market_close'].iloc[-1]}")

    if pd.Timestamp(dt.date.today(), tz='UTC') < nasdaq_schedule['market_close'].iloc[-1]:
        date_today = dt.datetime.combine(nasdaq_schedule.index[-2].date(), dt.time.min)
        return date_today
    else:
        return dt.datetime.combine(nasdaq_schedule.index[-1].date(), dt.time.min)