"""
Qhatu Twitter Bot.

Post BTC main market indicators and information for time frame 1d
Information source Binance API
requirements.txt < Tweepy 4.14.0

Requirements:
    conda create -n qhatu python=3.9.12 spyder-kernels=2.3
    conda activate qhatu
    pip3 install tweepy==3.7.0 pandas matplotlib
Stop using virtual environment
    conda deactivate
Remove virtual environment
    conda remove -n bbbot --all
    
Note: Kernel start error for console 1/A & 2/A > Start kernel 3/A
"""

# Libraries
import os
import tweepy
import time
from datetime import datetime
import logging
import libTA as libTA
import TAClass
import libGraphs as libGraphs

# Twitter keys
# They must be defined as environment variables before running this application
CONSUMER_KEY = str(os.environ.get('CONSUMER_KEY'))
CONSUMER_SECRET = str(os.environ.get('CONSUMER_SECRET'))
ACCESS_KEY = str(os.environ.get('ACCESS_KEY'))
ACCESS_SECRET = str(os.environ.get('ACCESS_SECRET'))

# Start log in file
logging.basicConfig(filename='./qhatubot.log', level=logging.INFO)
logging.info('*************************************************')
logging.info('Start %s' % time.ctime())

# Start Twitter session
tweepy_auth = tweepy.OAuth1UserHandler(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_KEY,
        ACCESS_SECRET)
tweepy_api = tweepy.API(tweepy_auth)

tweepy_client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_KEY,
    access_token_secret=ACCESS_SECRET
    )


# Files
def saveVariables(variableList):
    """ToDo."""
    f = open("qhatu.ini", "w+")
    for i in variableList:
        f.write("{}\n".format(i))
    f.close()


def readVariables():
    """ToDo."""
    try:
        f = open("qhatu.ini", "r")
        if f.mode == "r":
            contents = f.read()
            lines = contents.split('\n')
            # print(lines)
            if len(lines) < 3:
                return '', '', ''
            else:
                return lines[0], lines[1], lines[2]
    except Exception:
        return '', '', ''
    # print("")


# TA function, for technical analisys
def ta(symbol, interval):
    """ToDo."""
    # Get stock information from Binance API
    btcusdt = TAClass.TradeAsset(symbol, interval, 'Binance')
    btcusdt.getklines()
    btcusdt.dataframe()
    # If no error for stock information then continue, else return error
    if len(btcusdt.df.columns) >= 10:
        # Variable to use old libTA
        candles = btcusdt.klines
        # BB Bollinger Bands
        btcusdt.addsma(btcusdt.df, 20)
        middle = float(btcusdt.df['sma20'].iloc[-1])
        closestddev = float(
            1*btcusdt.df[len(btcusdt.df)-20:][['Close']].std(ddof=0))
        # upper = middle+2*closestddev
        lower = middle-2*closestddev
        lowbbl80 = middle-0.8*2*closestddev
        # RSI
        rsi = btcusdt.rsi(btcusdt.df, 14)
        # MACD
        macd, signal, hist = btcusdt.macd(btcusdt.df)
        # SMAs
        sma8 = btcusdt.sma(btcusdt.df, 8)
        sma20 = middle  # btcusdt.sma(btcusdt.df, 20)
        sma50 = btcusdt.sma(btcusdt.df, 50)
        sma100 = btcusdt.sma(btcusdt.df, 100)
        sma200 = btcusdt.sma(btcusdt.df, 200)
        # StochRSI
        k, d = libTA.stochRSI(candles)
        # Open time, Close price
        opentime2 = int(candles[len(candles)-1][0]/1000)-18000
        opentime2 = datetime.fromtimestamp(opentime2).strftime("%Y%m%d %H:%M")
        close2 = float(candles[len(candles)-1][4])
        # Return information, change number format depending on magnitude >1 <1
        if close2 >= 1.0:
            information = '%s %s:%.2f RSI(%.2f)' % (
                opentime2, symbol, close2, rsi)
            information = information + \
                ' StochRSI(%.2f,%.2f) macd(%.2f,%.2f)' % (k, d, macd, signal)
            information = information + \
                ' sma8:%.2f sma20:%.2f sma50:%.2f sma100:%.2f sma200:%.2f' % (
                    sma8, sma20, sma50, sma100, sma200)
        # Satoshis units if stock base is BTC
        elif symbol[len(symbol)-3:len(symbol)] == 'BTC':
            information = '%s %s(s):%.2f RSI(%.2f)' % (
                opentime2, symbol, close2*100000000, rsi)
            information = information + \
                ' StochRSI(%.2f,%.2f) macd(%.2f,%.2f)' % (
                    k, d, macd*100000000, signal*100000000)
            information = information + \
                ' sma8:%.2f sma20:%.2f sma50:%.2f sma100:%.2f sma200:%.2f' % (
                    sma8*100000000, sma20*100000000, sma50*100000000,
                    sma100*100000000, sma200*100000000)
        else:
            information = '%s %s:%.2E RSI(%.2f)' % (
                opentime2, symbol, close2, rsi)
            information = information + \
                ' StochRSI(%.2f,%.2f) macd(%.2E,%.2E)' % (k, d, macd, signal)
            information = information + \
                ' sma8:%.2E sma20:%.2E sma50:%.2E sma100:%.2E sma200:%.2E' % (
                    sma8, sma20, sma50, sma100, sma200)
        # Simple trend indicator
        # For 1d
        information2 = ''
        if interval == '1d':
            if sma8 >= sma20:
                if 0 < macd < signal:
                    information2 = 'possible flat 0ABC'
                elif macd > signal and k >= d:
                    information2 = 'possible uptrend strategy'
            else:
                if 0 > macd > signal:
                    information2 = 'possible flat 0ABC'
                elif macd < signal and k <= d:
                    information2 = 'possible downtrend strategy'
        # For 1w
        elif interval == '1w':
            if sma20 >= sma50:
                if close2 <= lowbbl80:
                    information2 = 'possible buy the dip strategy'
            else:
                if close2 <= lower and rsi <= 32:
                    information2 = 'possible buy the dip strategy'
        # Return information
        return information, information2
    else:
        return 'Network or API failure', ''


# Application
if __name__ == '__main__':
    # Use time frame 1d
    txt1d, txt1d2 = ta('BTCUSDT', '1d')
    # print(txt1d, txt1d2)
    # Check time frame 1w for a dip
    txt1w, txt1w2 = ta('BTCUSDT', '1w')
    # print(txt1w, txt1w2)
    # Text for twitter post
    if txt1d != 'Network or API failure' and txt1w != 'Network or API failure':
        # Check if TF 1w has a "buy the dip", else post TF 1d information
        if txt1w2 == 'possible buy the dip strategy':
            tf = '1w'
            txt = '#Bitcoin #Binance %s %s %s' % (tf, txt1w[15:], txt1w2)
        else:
            tf = '1d'
            txt = '#Bitcoin #Binance %s %s %s' % (tf, txt1d[15:], txt1d2)
    # Clear twitter api response
    response = ''
    # Post tweet
    try:
        response = tweepy_client.create_tweet(text=txt)
    except tweepy.errors.TweepyException as e:
        logging.info('%s %s\n%s' %
                     (time.strftime('%Y%m%d %H:%M:%S'), e, response))
    # Clear twitter api response
    response = ''
    # Post graph
    if time.strftime('%H') in ['00', '12']:
        libGraphs.smas_graph('BTCUSDT', '1d', 'Binance')
        try:            
            response = tweepy_api.update_status_with_media('#Bitcoin #Binance', './smas.png')
        except tweepy.errors.TweepyException as e:
            logging.info('%s %s\n%s' %
                         (time.strftime('%Y%m%d %H:%M:%S'), e, response))




