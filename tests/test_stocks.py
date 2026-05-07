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
# We don't pick the 1d period for obvious reasons - too short for tests like returns etc
test_period = all_periods[random.randint(1, len(all_periods) - 1)]
print(Fore.CYAN + f"Chosen period: {test_period}")


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
    
    # print(f"Dataframe columns:\n{exercise_data.columns}")

    assert column_truth and period_truth

# Flatten the dataframe to return only closing price data for the stocks
def test_filter_stocks_close(test_stock_data):
    # Exercise: Slice the dataframe
    close_data = utils.filter_stocks_close(test_stock_data)
    
    # Verification: Show that all tickers are there, and tuple length is 2
    close_data_tickers = [close_data.columns[i] for i in range(len(close_data.columns))]
    tickers_truth = all(ticker in test_stocks for ticker in close_data_tickers)
    
    length_truth = len(close_data.columns) == len(test_stocks)
    # print(f"close_data.cols: {list(close_data.columns)}")
    # print(f"test_stocks: {test_stocks}")
    
    assert tickers_truth and length_truth

# Should add daily returns based on the closing price in its own column
def test_filter_daily_close_returns(test_stock_data):
    # Exercise: apply the function to the df
    df_dcr = utils.filter_daily_close_return(test_stock_data)
    
    # Verification: pick a random stock, check a random day's return, check that the next day is correct
    random_security = test_stocks[random.randint(0, len(test_stocks) - 1)]
    random_initial_date_index = random.randint(0, len(df_dcr.index) - 2)
    initial_date = df_dcr.index[random_initial_date_index]
    next_date = df_dcr.index[random_initial_date_index + 1]
    # print(f"initial_date_index: {initial_date_index}")
    
    initial_close = test_stock_data.loc[initial_date, :]['Close'][random_security]
    # next_close_index = test_stock_data.loc[next_date_index, :].index + 1
    final_close = test_stock_data.loc[next_date, :]['Close'][random_security]
    control_return = (final_close / initial_close) - 1
    print(df_dcr.head())
    
    assert control_return == df_dcr.iloc[random_initial_date_index + 1][random_security]

# def test_add_daily_close_return(test_stock_data):
#     # Exercise: add the daily return column to each one that reflects the difference b/w closes
#     augmented_test_stock_data = test_stock_data.copy()
#     df_augmented = utils.add_daily_close_return(augmented_test_stock_data)
    
#     # Verification: Verify that close at iloc[0] * geoprod of all returns = price at iloc[-1] for random
#     random_stock = test_stocks[random.randint(0, len(test_stocks) - 1)]
#     c_initial_price = test_stock_data['Close'][random_stock].iloc[0]
#     c_final_price = test_stock_data['Close'][random_stock].iloc[-1]
    
#     total_geo_growth = ((df_augmented['Return'][random_stock] + 1).prod()) - 1
    
#     assert c_initial_price * (1 + total_geo_growth) == c_final_price

def test_flatten_yf_df(test_stock_data):
    # Exercise: Melt the dataframe into a date + ticker organized one
    # print(f"columns: {test_stock_data.columns}")
    # print(f"index: {test_stock_data.index}")
    # print(f"col level price: {test_stock_data.columns.get_level_values('Price')}")
    # print(f"col level ticker: {test_stock_data.columns.get_level_values('Ticker')}")
    df_molten = utils.flatten_yf_df(test_stock_data)
    
    # Verification: Verify that it is correctly uni-dimensional and has all columns
    c_cols = ['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']
    our_cols = list(df_molten.columns)
    
    # t_price_cols = test_stock_data.columns.get_level_values('Price')
    # t_ticker_cols = test_stock_data.columns.get_level_values('Ticker')
    # t_cols = t_price_cols + t_ticker_cols + ['Date']
    
    print(f"our cols:\n{our_cols}\n c_cols:\n {c_cols}")
    
    print(Fore.LIGHTYELLOW_EX + f"Stacked dataframe head: \n{df_molten.head(10)}")
    print(Fore.LIGHTYELLOW_EX + f"Stacked dataframe tail: \n{df_molten.head(10)}")
    
    assert all(val in our_cols for val in c_cols)