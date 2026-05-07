# API endpoints are exposed here

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, NaiveDatetime
from typing import List
from src import stocks, utils
import datetime as dt

# We define the interfaces

class Stock_Batch_Request(BaseModel):
    tickers: List[str]
    period: str

class YFinance_Record(BaseModel):
    Date: NaiveDatetime
    Ticker: str
    Close: float
    High: float
    Low: float
    Open: float
    Volume: float

# Initialize FastAPI
app = FastAPI()

# Test endpoint
@app.get('/')
def greeting():
    return {"message": "Dish is online"}

# Collect a batch of stocks
@app.post('/stocks/batch')
def release_batch(req: Stock_Batch_Request) -> List[YFinance_Record]:
    tickers, period = req.tickers, req.period
    df_payload = stocks.collect_stocks(tickers=tickers, period=period)
    df_flattened_payload = utils.flatten_yf_df(df_payload)
    print(f"DEBUG - Flattened payload head: \n{df_flattened_payload.head()}")
    payload = df_flattened_payload.to_dict(orient="records")
    print(f"DEBUG - Is DF Empty? {df_flattened_payload.empty}")
    print(f"DEBUG - DF Shape: {df_flattened_payload.shape}")
    print(f"DEBUG - Payload shape: {payload}")

    return payload