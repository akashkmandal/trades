#!/usr/bin/python3
import os
import talib
import pandas as pd
import matplotlib.pyplot as plt

# Define the path to the directory containing the CSV files
path = "./"

# Loop through each file in the directory
for filename in os.listdir(path):
    # Check if the file is a CSV file
    if filename.endswith(".csv"):
        # Load the CSV file into a Pandas DataFrame
        df = pd.read_csv(os.path.join(path, filename))

        # Check if the DataFrame has the necessary columns
        if all(col in df.columns for col in ['Date', 'Open', 'High', 'Low', 'Close']):
            # Rename the columns to match the expected format
            df = df.rename(columns={"Date": "date", "Open": "open", "High": "high", "Low": "low", "Close": "close"})

            # Convert the date column to a datetime object and set it as the DataFrame's index
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)

            # Calculate the ATR and add it as a new column to the DataFrame
            high_prices = df['high'].values
            low_prices = df['low'].values
            close_prices = df['close'].values
            atr = talib.ATR(high_prices, low_prices, close_prices, timeperiod=14)
            df['atr'] = atr

            # Calculate the EMA and add it as a new column to the DataFrame
            close_prices = df['close'].values
            ema = talib.EMA(close_prices, timeperiod=50)
            df['ema'] = ema

            # Find the rows where the close price is above the EMA and the EMA has positive slope
            if df["close"].iloc[-1] > ema[-1] and talib.SMA(ema, timeperiod=10)[-1] > 0:
                # Plot the ATR and EMA
                fig, ax = plt.subplots()
                ax.plot(df.index, df['atr'])
                ax.plot(df.index, df['ema'])
                ax.set_title(filename)
                plt.show()
        else:
            print(f"{filename} does not have the necessary columns")
    else:
        print(f"{filename} is not a CSV file")

