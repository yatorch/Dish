# Decorators for logging purposes
import time
from colorama import Fore, Style
from functools import wraps
import asyncio

# Anything on the yfinance API needs to be non-async, due to the API's usage of the requests library UTH

def log_time_sync_fetch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(Fore.GREEN + f"Executing {func.__name__}")
        start_time = time.perf_counter()

        output = func(*args, **kwargs)

        end_time = time.perf_counter()
        print(Fore.GREEN + f"Executed {func.__name__} in {end_time - start_time}s")
        return output
    return wrapper

# CPU-Heavy calculations will not be asynchronous, as opposed to I/O fetching from databases

def log_time_calc(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(Fore.GREEN + f"Executing {func.__name__}")
        start_time = time.perf_counter()

        output = func(*args, **kwargs)

        end_time = time.perf_counter()
        print(Fore.GREEN + f"Executed {func.__name__} in {end_time - start_time}s")
        return output
    return wrapper