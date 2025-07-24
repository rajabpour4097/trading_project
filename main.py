# main.py
import pandas as pd
import numpy as np
from strategy import TradingStrategy
from logger import log
from time import sleep

strategy = TradingStrategy()

log("App started...", color='green')
last_data = None

while True:
    try:
        data = pd.read_csv("eurusd_prices_multiip.csv", parse_dates=["timestamp"], index_col="timestamp")
        data['status'] = np.where(data['open'] > data['close'], 'bearish', 'bullish')

        if last_data is None or data.iloc[-1].name != last_data.name:
            strategy.update_legs(data)
            strategy.handle_swing(data)
            last_data = data.iloc[-1]

        sleep(0.5)

    except Exception as e:
        log(f"Unhandled error: {e}", color='red')
