#!/bin/usr/env python3
from bs4 import BeautifulSoup as bs
import csv
import requests

LSE = 'https://www.lse.co.uk/SharePrice.asp?shareprice='

def get_stocks():
    with open('tickers.csv') as ticker_file:
        return list(map(lambda ticker: ticker.strip(), ticker_file))

def to_csv(stocks):
    with open('stocks.csv', 'w') as sectors:
        writer = csv.writer(sectors)
        writer.writerow(stocks[0].keys())
        for stock in stocks:
            writer.writerow(stock.values())

def get_soup(url):
    return bs(requests.get(url).text, 'html.parser')
    
def get_sector(ticker):
    soup = get_soup(LSE + ticker)
    try: 
        share_details = soup.find_all('p', attrs={'class', 
                                      'sp-share-details__text'})[1]
        sector = share_details.find('a').text
    except:
        print('No sector information availible for ', ticker)
        return { 'ticker': ticker, 'sector': ''}

    print(ticker, sector)
    return { 'ticker': ticker, 'sector': sector}


if __name__ == '__main__':
    to_csv(list(map(lambda ticker: get_sector(ticker), get_stocks())))
