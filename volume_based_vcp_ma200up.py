#!/usr/bin/python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import talib

# Define directory path
dir_path = './'

# Loop through all files in directory
for filename in os.listdir(dir_path):
    if filename.endswith('.csv'):
        # Load data from CSV file into DataFrame
        data = pd.read_csv(os.path.join(dir_path, filename))

        # Check that DataFrame has correct columns
        expected_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        if not all(elem in data.columns for elem in expected_columns):
            print(f"Error: Invalid columns in file {os.path.join(dir_path, filename)}")
            continue

        # Check if data is from last 6 months
        last_six_months = pd.Timestamp.today() - pd.DateOffset(months=6)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.loc[data['Date'] >= last_six_months]

        # Check if stock is above 200-day moving average
        ma200 = talib.SMA(data['Close'], timeperiod=200)
        if data['Close'].iloc[-1] < ma200.iloc[-1]:
            continue

        # Check if stock is in uptrend
        ema9 = talib.EMA(data['Close'], timeperiod=9)
        ema21 = talib.EMA(data['Close'], timeperiod=21)
        if ema9.iloc[-1] < ema21.iloc[-1]:
            continue

        # Check if data meets volatility contraction criteria
        num_contractions = 0
        prev_contraction = 0
        for i in range(1, len(data)):
            current_range = data.iloc[i]['High'] - data.iloc[i]['Low']
            prev_range = data.iloc[i-1]['High'] - data.iloc[i-1]['Low']
            current_volume = data.iloc[i]['Volume']
            prev_volume = data.iloc[i-1]['Volume']
            if current_range < prev_range and current_volume < prev_volume:
                num_contractions += 1
                if num_contractions > 1 and current_range >= prev_contraction:
                    break
                prev_contraction = current_range
            elif current_range >= prev_range or current_volume >= prev_volume:
                num_contractions = 0

            if num_contractions == 6:
                break

        if num_contractions >= 2 and num_contractions <= 6:
            # Plot chart of stock's daily candle
            fig, ax = plt.subplots()
            ax.plot(data['Date'], data['High'], color='green', label='High')
            ax.plot(data['Date'], data['Low'], color='red', label='Low')
            ax.set_title(f"{filename.split('.')[0]} Daily Candle")
            ax.legend()
            plt.show()
