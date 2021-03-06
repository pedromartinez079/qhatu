"""
Qhatu Twitter Bot.

Post BTC main market indicators and information
For time frame 4h every hour
For time frame 1d at UTC 02, 08, 14, 20 hours
Information source Binance API
Tweepy 3.7.0
Update code for Tweepy 4.4.0!
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
# tweepy.debug(True)
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
# api = tweepy.API(auth, wait_on_rate_limit=True,
#                   wait_on_rate_limit_notify=True)
api = tweepy.API(auth)


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
        # RSI
        rsi = btcusdt.rsi(btcusdt.df, 14)
        # MACD
        macd, signal, hist = btcusdt.macd(btcusdt.df)
        # SMAs
        sma8 = btcusdt.sma(btcusdt.df, 8)
        sma21 = btcusdt.sma(btcusdt.df, 21)
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
                ' sma8:%.2f sma21:%.2f sma50:%.2f sma100:%.2f sma200:%.2f' % (
                    sma8, sma21, sma50, sma100, sma200)
        # Satoshis units if stock base is BTC
        elif symbol[len(symbol)-3:len(symbol)] == 'BTC':
            information = '%s %s(s):%.2f RSI(%.2f)' % (
                opentime2, symbol, close2*100000000, rsi)
            information = information + \
                ' StochRSI(%.2f,%.2f) macd(%.2f,%.2f)' % (
                    k, d, macd*100000000, signal*100000000)
            information = information + \
                ' sma8:%.2f sma21:%.2f sma50:%.2f sma100:%.2f sma200:%.2f' % (
                    sma8*100000000, sma21*100000000, sma50*100000000,
                    sma100*100000000, sma200*100000000)
        else:
            information = '%s %s:%.2E RSI(%.2f)' % (
                opentime2, symbol, close2, rsi)
            information = information + \
                ' StochRSI(%.2f,%.2f) macd(%.2E,%.2E)' % (k, d, macd, signal)
            information = information + \
                ' sma8:%.2E sma21:%.2E sma50:%.2E sma100:%.2E sma200:%.2E' % (
                    sma8, sma21, sma50, sma100, sma200)
        # Simple trend indicator
        # For 1d
        if interval == '1d':
            if sma8 > sma21:
                if 0 < macd < signal:
                    information = information+' possible flat 0ABC'
                elif k > d:
                    information = information+' possible uptrend strategy'
            else:
                if macd > signal and close2 <= lower:
                    information = information+' possible buy the dip strategy'
        # For 4h
        elif interval == '4h':
            if sma21 >= sma200:
                if 0 < macd < signal:
                    information = information+' possible flat 0ABC'
                elif k > d:
                    information = information+' possible uptrend strategy'
                elif close2 <= lower:
                    information = information+' possible buy the dip strategy'
            else:
                if close2 <= lower:
                    information = information+' possible buy the dip strategy'
        # Return information
        return information
    else:
        return 'Network or API failure'


# Application loop control
while True:
    # Check time hour for UTC[02,08,14,20], UTC-5 [03,09,15,21]
    # if true apply time frame 1d
    hourlist = ['02', '08', '14', '20']
    if time.strftime('%H') in hourlist:
        # Get information using TA function
        txt = ta('BTCUSDT', '1d')
        # txt = ta('BNBBTC', '4h')
        # Set time frame 1d
        tf = '1d'
    else:
        # Get information using TA function
        txt = ta('BTCUSDT', '4h')
        # txt = ta('BNBBTC', '4h')
        # Set time frame 4h
        tf = '4h'
    if txt != 'Network or API failure':
        txt = '#Bitcoin Binance %s %s' % (tf, txt[15:])
    # Clear twitter api response
    response = ''
    # Post tweet
    try:
        response = api.update_status(txt)
        # print(response)
    except tweepy.TweepError as e:
        logging.info('%s %s\n%s' %
                     (time.strftime('%Y%m%d %H:%M:%S'), e, response))
    # Clear twitter api response
    response = ''
    # Post graph
    if time.strftime('%H') in ['00', '12']:
        libGraphs.smas_graph('BTCUSDT', '1d', 'Binance')
        try:
            response = api.update_with_media('./smas.png', '#Bitcoin')
        except tweepy.TweepError as e:
            logging.info('%s %s\n%s' %
                         (time.strftime('%Y%m%d %H:%M:%S'), e, response))
    # Wait one hour to for next post
    time.sleep(3600)
