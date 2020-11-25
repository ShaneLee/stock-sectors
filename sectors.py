#!/bin/usr/env python3
from pandas_datareader import data
import pandas as pd
import numpy as np
from datetime import datetime
import csv

def to_csv(stocks):
    with open('sector_data.csv', 'w') as sectors:
        writer = csv.writer(sectors)
        writer.writerow(stocks[0].keys())
        for stock in stocks:
            writer.writerow(stock.values())


def reindex_column(panel_data, key, all_weekdays):
  column = panel_data[key].reindex(all_weekdays)
  return column.fillna(method='ffill')

def replace_dot(ticker):
  return ticker.replace('.', '-') + '.L'

def check_dot(ticker):
  if '.' in ticker[-1]:
    return ticker + 'L'
  elif '.'in ticker[-2]:
    return replace_dot(ticker)
  else: 
    return ticker + '.L'

def get_sectors():
    with open('stocks.csv') as stocks_file:
        return dict(map(lambda x: [x.split(',')[0].strip(),
                                   x.split(',')[1].strip()],
                                   stocks_file)) 

def get_last_year(ticker, sector):
    ticker_l = check_dot(ticker)
    now = datetime.now()
    end_date = str(now.strftime('%Y-%m-%d'))

    start_date = str(now.replace(year = now.year -1).strftime('%Y-%m-%d'))
    all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')

    try: 
        panel_data = data.DataReader(ticker_l, 'yahoo', start_date, end_date)
        adj_close = reindex_column(panel_data, 'Adj Close', all_weekdays)
        current_price = np.mean(adj_close.tail(1))
        annual_return = (current_price / np.mean(adj_close.head(1))) * 100

        return {
            'ticker': ticker, 
            'sector': sector, 
            'date': end_date, 
            'current_price': current_price,
            'annual_return': annual_return
            }
    except:
        print('Error for ', ticker_l)


if __name__ == '__main__':
    stock_data = []
    stocks = get_sectors()
    for key, sector in stocks.items():
        if not sector:
            continue
        if 'ticker' not in key:
            stock_data.append(get_last_year(key, sector))
    to_csv(stock_data)
