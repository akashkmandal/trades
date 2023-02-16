#!/usr/bin/python3
import os
import csv

# Function to create the trade journal CSV file if it doesn't already exist
def create_trade_journal_csv():
    if not os.path.exists('trade_journal.csv'):
        with open('trade_journal.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Symbol', 'Type', 'Entry Date', 'Entry Price', 'Exit Date', 'Exit Price', 'Shares', 'Commission', 'Profit/Loss'])

# Function to add a new trade entry to the CSV file
def add_trade_entry_to_csv(symbol, trade_type, entry_date, entry_price, exit_date, exit_price, shares, commission):
    # Calculate profit/loss
    profit_loss = (exit_price - entry_price) * shares - commission

    # Open the CSV file and append the new trade entry
    with open('trade_journal.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([symbol, trade_type, entry_date, entry_price, exit_date, exit_price, shares, commission, profit_loss])

# Function to calculate the total profit/loss for all trades in the CSV file
def calculate_total_profit_loss():
    total_pl = 0
    with open('trade_journal.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader) # skip header row
        for row in reader:
            pl = float(row[8])
            total_pl += pl
    return total_pl

# Check if the CSV file exists, and create it if it doesn't
create_trade_journal_csv()

# Prompt the user to enter a new trade entry
symbol = input('Enter the symbol for the trade: ')
trade_type = input('Enter the type of trade (buy/sell): ')
entry_date = input('Enter the entry date (YYYY-MM-DD): ')
entry_price = float(input('Enter the entry price: '))
exit_date = input('Enter the exit date (YYYY-MM-DD, or leave blank if not yet sold): ')
exit_price = float(input('Enter the exit price, or leave blank if not yet sold: ') or '0')
shares = int(input('Enter the number of shares: '))
commission = float(input('Enter the commission, or enter 0 if there was none: ') or '0')

# Add the new trade entry to the CSV file
add_trade_entry_to_csv(symbol, trade_type, entry_date, entry_price, exit_date, exit_price, shares, commission)

# Calculate the total profit/loss for all trades
total_pl = calculate_total_profit_loss()
print('Total profit/loss: $', total_pl)

