# To test the stocks module

import pytest
import datetime as dt
import random
from pytickersymbols import PyTickerSymbols
from tabulate import tabulate
import pandas_market_calendars as mcal
import yfinance as yf
from colorama import Fore
from src import stocks
from src import utils



date_today = utils.get_latest_mclose_date()
print('DATE TODAY: ' + str(date_today))
# date_today = dt.datetime.combine(dt.date.today(), dt.time.min)
date_today_str = dt.date.today().strftime("%Y-%m-%d")


# We pick a random number of stocks and a random period
pyticker_stocks = PyTickerSymbols()
all_tickers = [stock['symbol'] for stock in pyticker_stocks.get_stocks_by_index('NASDAQ 100')]

no_stocks = random.randint(3, 5)
test_stocks = [all_tickers[random.randint(0, 94) + i] for i in range(no_stocks + 1)]
print(Fore.CYAN + f"Chosen stocks: {" and ".join(test_stocks)}")

all_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
test_period = all_periods[random.randint(0, len(all_periods) - 1)]


@pytest.fixture(scope="module")
def test_stock_data():
    df_fixture = yf.download(tickers=test_stocks, period=test_period, auto_adjust=True)
    return df_fixture


# collect_stocks() for a certain period. Since data may change, we check tickers and columns only
def test_collect_stocks():
    # Setup: collect 3-5 random tickers from the generated tickers, and select a random period. Done above


    # Exercise: call the function to get the stock data for a random period
    exercise_data = stocks.collect_stocks(test_stocks, test_period)
    print(Fore.GREEN + f"Collected stocks")

    # Verify: check that the column names include the stocks, and that the period matches
    column_tickers = [exercise_data.columns[i][1] for i in range(len(exercise_data.columns))]
    column_truth = all(ticker in list(column_tickers) for ticker in test_stocks)
    
    time_indices = list(exercise_data.index)
    actual_time_difference = date_today - exercise_data.index[0]
    dataset_time_difference = exercise_data.index[-1] - exercise_data.index[0]

    period_truth = actual_time_difference == dataset_time_difference

    assert column_truth and period_truth

# Flatten the dataframe to return only closing price data for the stocks
def test_filter_stocks_close(test_stock_data):
    # Exercise: Slice the dataframe
    close_data = utils.filter_stocks_close(test_stock_data)
    
    # Verification: Show that all tickers are there, and tuple length is 2
    close_data_tickers = [close_data.columns[i] for i in range(len(close_data.columns))]
    tickers_truth = all(ticker in test_stocks for ticker in close_data_tickers)
    
    length_truth = len(close_data.columns) == len(test_stocks)
    
    assert tickers_truth and length_truth

