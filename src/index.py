# API endpoints are exposed here

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from src import stocks, utils

# We define the interfaces

class Stock_Batch(BaseModel):
    tickers: List[str]
    period: str

# Initialize FastAPI
app = FastAPI()

# Test endpoint
@app.get('/')
def greeting():
    return {"message": "Dish is online"}

# Collect a batch of stocks
@app.post('/stocks/batch')
def release_batch(req: Stock_Batch):
    tickers, period = req.tickers, req.period
    df_payload = stocks.collect_stocks(tickers=tickers, period=period)
    df_flattened_payload = utils.flatten_yf_df(df_payload)
    payload = df_flattened_payload.to_dict(orient="records")
    print(f"DEBUG - Is DF Empty? {df_flattened_payload.empty}")
    print(f"DEBUG - DF Shape: {df_flattened_payload.shape}")
    return {"data": payload}