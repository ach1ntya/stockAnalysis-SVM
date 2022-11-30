from bs4 import BeautifulSoup
import datetime
import json
import numpy as np
import pandas as pd
import requests
import time
import warnings
warnings.simplefilter('ignore')

import talib as ta
from talib import MA_Type

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import svm

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker

start_Date = int(time.mktime((2017,10,28,4,0,0,0,0,0)))
end_Date = int(time.mktime((2022,10,28,4,0,0,0,0,0)))

#Dow Jones Industrial Average Component tickers
tickersList = ["AXP", "AMGN", "AAPL", "BA", "CAT", "CSCO", "CVX",
               "GS", "HD", "HON", "IBM", "INTC", "JNJ", "KO",
               "JPM", "MCD", "MMM", "MRK", "MSFT", "NKE", "PG", "CRM", "TRV", 
               "UNH", "VZ", "V", "WBA", "WMT", "DIS", "DOW"]

print(len(tickersList))

def scrapeYahoo(data_df, ticker, start_date, end_date):
    Base_Url = 'https://query1.finance.yahoo.com/v8/finance/chart/'
    Scrape_Url = Base_Url + ticker + "?period1=" + str(start_date)+"&period2="+str(end_date)+"&interval=1d"
    
    r = requests.get(Scrape_Url)
    Page_Data = r.json()
    stock_df = pd.DataFrame()
    stock_df["DateTime"] = Page_Data["chart"]["result"][0]["timestamp"]
    stock_df['DateTime'] = stock_df['DateTime'].apply(lambda x: datetime.datetime.fromtimestamp(x).date().isoformat())
    stock_df["Open"] = Page_Data["chart"]["result"][0]["indicators"]["quote"][0]["open"]
    stock_df["High"] = Page_Data["chart"]["result"][0]["indicators"]["quote"][0]["high"]
    stock_df["Low"] = Page_Data["chart"]["result"][0]["indicators"]["quote"][0]["low"]
    stock_df["Close"] = Page_Data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    stock_df["Volume"] = Page_Data["chart"]["result"][0]["indicators"]["quote"][0]["volume"]
    stock_df = stock_df.set_index("DateTime")
    
    data_df[ticker] = stock_df

stockData = {}
for tickers in tickersList:
    scrapeYahoo(stockData, tickers, start_Date, end_Date)
    print(tickers + "done")
    time.sleep(0.5)
    
for tickers in tickersList:
    stockData[tickers]["High Shifted"] = stockData[tickers]["High"].shift(-1)
    stockData[tickers]["Low Shifted"] = stockData[tickers]["Low"].shift(-1)
    stockData[tickers]["Close Shifted"] = stockData[tickers]["Close"].shift(-1)
    
    stockData[tickers]["Upper Band"], stockData[tickers]["Middle Band"], stockData[tickers]["Lower Band"] = ta.BBANDS(stockData[tickers]["Close Shifted"], timeperiod=20)
    stockData[tickers]["RSI"] = ta.RSI(stockData[tickers]["Close Shifted"], timeperiod=14)
    stockData[tickers]["MACD"], stockData[tickers]["MACD Signal"], stockData[tickers]["MACD Hist"] = ta.MACD(stockData[tickers]["Close Shifted"], fastperiod=12, slowperiod=26, signalperiod=9)
    stockData[tickers]["Momentum"] = ta.MOM(stockData[tickers]["Close Shifted"], timeperiod=12)
    stockData[tickers]["Returns"] = np.log(stockData[tickers]["Open"] / stockData[tickers]["Open"].shift(1))

for tickers in tickersList:
    signals = []
    for j in stockData
    
    

     
    


