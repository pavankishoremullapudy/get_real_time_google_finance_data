# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 02:28:32 2016

@author: pmullapudy
"""
# Imports
from datetime import datetime
import pandas as pd
import requests
#
# Functions
def get_intraday_google_data(symbol, interval_minutes, num_days):
    #
    exchange = 'NSE'
    interval_seconds_increment = (interval_minutes*60) + 1
    #
    url_string = ('http://www.google.com/finance/getprices?i='
                + str(interval_seconds_increment) + '&p=' + str(num_days)
                + 'd&f=d,o,h,l,c,v&df=cpct&x=' + exchange.upper()
                + '&q=' + symbol.upper())

    # use requests to get url_root
    try:
        r = requests.get(url_string, timeout=3.05)
    except requests.exceptions.HTTPError as hte:
        print ("HTTPError exception for symbol:", symbol, hte)
        return
    except requests.exceptions.ConnectionError as ce:
        print ("ConnectionError exception for symbol:", symbol, ce)
        return
    except requests.exceptions.ConnectTimeout as cte:
        print ("ConnectTimeout exception for symbol:", symbol, cte)
        return
    except requests.exceptions.ReadTimeout as rte:
        print ("ReadTimeout exception for symbol:", symbol, rte)
        return
    except:
        print ("Unknown exception for symbol:", symbol)
        return
    else:
        stock_str = str(r.text)
        stock_list = stock_str.split('\n')
        if stock_list[len(stock_list)-1] == "": # delete the last blank list
            del stock_list[-1]
        if len(stock_list) < 7: # In case the stock list has no OHLC data
            print ("stock list has no OHLC data for: ", symbol)
            return
        stock_list = stock_list[7:]
        stock_list = [line.split(',') for line in stock_list]
        #
        df = pd.DataFrame(stock_list, columns=['Date_Time','Close','High','Low','Open','Volume'])
        # Convert UNIX format to Datetime format
        df['Date_Time'] = df['Date_Time'].apply(lambda x: datetime.fromtimestamp(int(x[1:])))
        #
        df['Open'] = df['Open'].astype(float).apply(lambda x: round(x,2))
        df['High'] = df['High'].astype(float).apply(lambda x: round(x,2))
        df['Low'] = df['Low'].astype(float).apply(lambda x: round(x,2))
        df['Close'] = df['Close'].astype(float).apply(lambda x: round(x,2))
        #
        df['Volume'] = df['Volume'].astype(int)

        # make datetime as the index and drop  the column
        df = df.set_index(['Date_Time'], drop=True)

        # Reorder to OHLCV format
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        #
        return df
#
# Main Program
df = get_intraday_google_data('TCS', 5, 2)