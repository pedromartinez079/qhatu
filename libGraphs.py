# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 17:50:08 2021

@author: Dropex
"""

import TAClass
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def smas_graph(symbol,interval,exchange):
    asset = TAClass.TradeAsset(symbol,interval,exchange)
    asset.getklines()
    asset.dataframe()
    asset.addsma(asset.df, 10)
    asset.addsma(asset.df, 20)
    asset.addsma(asset.df, 50)
    asset.addsma(asset.df, 100)
    asset.addsma(asset.df, 200)
    
    opentime_df=pd.to_datetime(asset.df['OpenTime'], unit='ms')
    x=np.asanyarray(opentime_df)
    y1=np.asanyarray(asset.df[:][['Close']])
    y10=np.asanyarray(asset.df[:][['sma10']])
    y20=np.asanyarray(asset.df[:][['sma20']])
    y50=np.asanyarray(asset.df[:][['sma50']])
    y100=np.asanyarray(asset.df[:][['sma100']])
    y200=np.asanyarray(asset.df[:][['sma200']])
    plt.figure(figsize=(8,4))
    plt.plot(x, y1, label='ClosePrice', color='lightgrey')
    plt.plot(x, y10, label='sma10')
    plt.plot(x, y20, label='sma20')
    plt.plot(x, y50, label='sma50')
    plt.plot(x, y100, label='sma100')
    plt.plot(x, y200, label='sma200')
    plt.title('SMAs '+interval)
    plt.xlabel("OpenTime")
    plt.ylabel("Price")
    plt.legend()
    plt.savefig('smas.png')
    plt.close("all")
    
def rsi_graph(symbol,interval,exchange):
    asset = TAClass.TradeAsset(symbol,interval,exchange)
    asset.getklines()
    asset.dataframe()
    asset.addrsi(asset.df)
    
    opentime_df=pd.to_datetime(asset.df['OpenTime'], unit='ms')
    x=np.asanyarray(opentime_df)
    y=np.asanyarray(asset.df[:][['rsi14']])
    plt.figure(figsize=(8,4))
    plt.plot(x, y, label='RSI', color='blue')
    plt.axhline(y = 70, color = 'grey', linestyle = 'dashed')
    plt.axhline(y = 30, color = 'grey', linestyle = 'dashed')
    plt.title('RSI '+interval)
    plt.xlabel("OpenTime")
    plt.ylabel("RSI")
    plt.legend()
    plt.savefig('rsi.png')
    plt.close("all")
    
def macd_graph(symbol,interval,exchange):
    asset = TAClass.TradeAsset(symbol,interval,exchange)
    asset.getklines()
    asset.dataframe()
    asset.addmacd(asset.df)
    
    opentime_df=pd.to_datetime(asset.df['OpenTime'], unit='ms')
    x=np.asanyarray(opentime_df)
    y1=np.asanyarray(asset.df[:][['macd']])
    y2=np.asanyarray(asset.df[:][['signal']])
    y3=np.asanyarray(asset.df[:][['histogram']])
    plt.figure(figsize=(8,4))
    plt.plot(x, y1, label='macd', color='blue')
    plt.plot(x, y2, label='signal', color='red')
    plt.plot(x, y3, label='histogram', color='lightgrey')
    plt.axhline(y = 0, color = 'black', linestyle = '-')
    plt.title('MACD '+interval)
    plt.xlabel("OpenTime")
    plt.ylabel("MACD")
    plt.legend()
    plt.savefig('macd.png')
    plt.close("all")

def adx_graph(symbol,interval,exchange):
    asset = TAClass.TradeAsset(symbol,interval,exchange)
    asset.getklines()
    asset.dataframe()
    asset.addadx(asset.df)
    
    opentime_df=pd.to_datetime(asset.df['OpenTime'], unit='ms')
    x=np.asanyarray(opentime_df)
    y1=np.asanyarray(asset.df[:][['adx']])
    y2=np.asanyarray(asset.df[:][['upDI']])
    y3=np.asanyarray(asset.df[:][['downDI']])
    plt.figure(figsize=(8,4))
    plt.plot(x, y1, label='adx', color='red')
    plt.plot(x, y2, label='+DI', color='lightblue')
    plt.plot(x, y3, label='-DI', color='lightgrey')
    plt.axhline(y = 23, color = 'black', linestyle = 'dashed', label='Key Level')
    plt.title('ADX '+interval)
    plt.xlabel("OpenTime")
    plt.ylabel("ADX,+DI,-DI")
    plt.legend()
    plt.savefig('adx.png')
    plt.close("all")
