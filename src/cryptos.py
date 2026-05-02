# For fetching cryptocurrency data. Targets are stablecoins and highly liquid altcoins

import pandas as pd
import ccxt.async_support as ccxt
import src.apimw as apimw
import os
from dotenv import load_dotenv
import asyncio

# We load our exchange related keys here before initializing CCXT and friends
load_dotenv()

# We now initialize the relevant exchanges via CCXT

binance_exchange = ccxt.binance({
    'apiKey': os.getenv('BINANCE_API_KEY'),
    'secret': os.getenv('BINANCE_API_SECRET'),
    'enableRateLimit': True,
    'options':{
        'defaultType': 'spot',
        'adjustForTimeDifference': True
    }
})

# We now define methods for fetching data
