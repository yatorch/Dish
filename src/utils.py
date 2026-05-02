# Utility funcs

import datetime as dt
from datetime import timezone
import pandas_market_calendars as mcal
import pandas as pd


def get_latest_mclose_date():
    nasdaq_calendar = mcal.get_calendar('NASDAQ')
    date_today_raw = dt.date.today()
    start_date_nd = date_today_raw - dt.timedelta(days=7)
    nasdaq_schedule = nasdaq_calendar.schedule(start_date=start_date_nd, end_date=date_today_raw)
    print(f"last market close: {nasdaq_schedule['market_close'].iloc[-1]}")
    print(f"last market open: {nasdaq_schedule['market_open'].iloc[-1]}")
    now = dt.datetime.now(timezone.utc)
    chour = now.hour
    cmin = now.minute
    csec = now.second
    
    print(f"current time: {pd.Timestamp(now, hour=chour, minute=cmin, second=csec)}")

    if pd.Timestamp(now) < nasdaq_schedule['market_open'].iloc[-1]:
        date_today = dt.datetime.combine(nasdaq_schedule.index[-2].date(), dt.time.min)
        return date_today
    else:
        return dt.datetime.combine(nasdaq_schedule.index[-1].date(), dt.time.min)

def filter_stocks_close(df):
    return df['Close']

# Returns a copy of the dataframe that only has daily close returns for each security
def filter_daily_close_return(df):
    df_copy = df.copy()
    df_dcr = df_copy['Close'].pct_change().dropna().bfill().ffill()
    return df_dcr

# Adds a returns column to the 2d yf.downloads() df that has returns on closes for each security
def add_daily_close_return(df):
    df['Return'] = df['Close'].pct_change()
    return df