import pandas as pd
import yfinance as yf
import datetime as dt
import src.apimw as apimw
import asyncio

@apimw.log_time_sync_fetch
def collect_stocks(tickers, period = '1y', start_date = 0, end_date = 0):
    end_date = dt.date.today().strftime('%Y-%m-%d') if end_date == 0 else end_date

    if start_date == 0:
        data = yf.download(tickers=tickers, period=period, auto_adjust=True)
        return data
    
    data = yf.download(tickers=tickers, start=start_date, end=end_date, auto_adjust=True)
    return data

