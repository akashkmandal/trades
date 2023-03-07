#!/usr/bin/python3
import pandas as pd
import mplfinance as mpf
import os

data_path = "./"

ema_length = 20
days_above_ema = 3

valid_dfs = []
for filename in os.listdir(data_path):
    if filename.endswith(".NS.csv"):
        df = pd.read_csv(os.path.join(data_path, filename))
        stock_name = os.path.splitext(os.path.basename(filename))[0]
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        df['EMA'] = df['Close'].ewm(span=ema_length).mean()
        last_n_days = df.iloc[-days_above_ema:]
        if all(last_n_days['Close'] >= last_n_days['EMA']):
            valid_dfs.append((df, stock_name))

#for df, stock_name in valid_dfs:
#    mpf.plot(df, type='candle', mav=(ema_length,), volume=True, title=f"{stock_name} - 20EMA Strategy", figsize=(15, 10))
for df, stock_name in sorted(valid_dfs, key=lambda x: x[1], reverse=True):
    mpf.plot(df, type='candle', mav=(ema_length,), volume=True, title=f"{stock_name} - 20EMA Strategy", figsize=(15, 10))


