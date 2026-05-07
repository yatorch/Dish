# To test the API endpoints

import pytest
import datetime as dt
import random
from pytickersymbols import PyTickerSymbols
from tabulate import tabulate
import pandas_market_calendars as mcal
import pandas as pd
import yfinance as yf
from colorama import Fore
from src import stocks
from src import utils
import httpx
import json

API_LINK = 'http://127.0.0.1:8000/'

# Collecting random stocks

pyticker_stocks = PyTickerSymbols()
all_tickers = [stock['symbol'] for stock in pyticker_stocks.get_stocks_by_index('NASDAQ 100')]

no_stocks = random.randint(3, 5)
test_stocks = [all_tickers[random.randint(0, 94) + i] for i in range(no_stocks + 1)]
print(Fore.MAGENTA + f"Chosen stocks [API TEST]: {" and ".join(test_stocks)}")

period='5d'

# Structure of basic returned data for batch
basic_columns = ['Date', 'Ticker', 'Close', 'High', 'Low', 'Open', 'Volume']

# # Actual download from yfinance as a fixture
# @pytest.fixture(scope="module")
# def test_stock_data():
#     df_fixture = yf.download(tickers=test_stocks, period=test_period, auto_adjust=True)
#     return df_fixture

# Basic test to see if online

def test_ping():
    response = httpx.get(f"{API_LINK}")

    assert response.status_code == 200

# Basic test to see if data is fetched correctly

def test_endpoint_collect_stocks():
    payload = {
        "tickers": test_stocks,
        "period": period
    }
    response = httpx.post(API_LINK + "stocks/batch", json=payload)
    print(Fore.MAGENTA + f"response object: \n{response}")
    parsed_response = response.json()
    df = pd.DataFrame.from_records(parsed_response)

    print(Fore.MAGENTA + f"Response body: \n{df.head()}")

    assert all(col in df.columns for col in basic_columns)