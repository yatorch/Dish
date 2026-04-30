# To test the stocks module

import pytest
import datetime as dt
import random
from tabulate import tabulate
import itertools
from pytickersymbols import PyTickerSymbols
import pandas_market_calendars as mcal
from colorama import Fore
from src import stocks
from src import utils

pyticker_stocks = PyTickerSymbols()
all_tickers = [stock['symbol'] for stock in pyticker_stocks.get_stocks_by_index('NASDAQ 100')]

date_today = utils.get_latest_mclose_date()
print('DATE TODAY: ' + str(date_today))
# date_today = dt.datetime.combine(dt.date.today(), dt.time.min)
date_today_str = dt.date.today().strftime("%Y-%m-%d")

# collect_stocks() for a certain period
def test_collect_stocks():
    # Setup: collect 3-5 random tickers from the generated tickers, and select a random period.
    no_stocks = random.randint(3, 5)
    test_stocks = [all_tickers[random.randint(0, 94) + i] for i in range(no_stocks + 1)]
    print(Fore.CYAN + f"Chosen stocks: {" and ".join(test_stocks)}")

    all_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    test_period = all_periods[random.randint(0, len(all_periods) - 1)]

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