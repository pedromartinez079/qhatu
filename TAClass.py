# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 16:18:13 2020

@author: Dropex
"""
import sys
import requests
import pandas as pd
import numpy as np

class TradeAsset:
    """
    symbol: BTCUSDT, XAUUSD, AMZN, etc.
    interval: 1h, 4h, 1d, etc.
    exchange: Binance, BitMex, ByBit, etc.
    """
    def __init__(self, symbol, interval, exchange):
        self.symbol = symbol
        self.interval = interval
        self.exchange = exchange
        
    #Use exchange API to get market information
    def getklines(self):
        if self.exchange == 'Binance':
            url_base='https://api.binance.com/api/v1/klines'
            PARAMS = {'symbol':self.symbol, 'interval':self.interval}
            myheaders = {}
            try:
                myrequest = requests.get(url = url_base, headers = myheaders, params = PARAMS)
                self.klines = myrequest.json()
            except:
                self.klines = [sys.exc_info()[0]]
        else:
            self.klines = ['Exchange not defined']
    
    #Generate pandas dataframe for further analysis
    def dataframe(self):
        df=pd.DataFrame(self.klines)
        dfcolumns=len(df.columns) >= 12
        if dfcolumns and self.exchange == 'Binance':
            df.columns=['OpenTime','Open','High','Low','Close','Volume','CloseTime','QuoteAssetVol','NoOfTrades','BuyVolume','TakerbuyquoteassetVol','Nothing']
            df=df[['OpenTime','Open','High','Low','Close','Volume','CloseTime','BuyVolume']]
            df[['Open','High','Low','Close','Volume','BuyVolume']] = df[['Open','High','Low','Close','Volume','BuyVolume']].astype(float)
            df['SellVolume']=df['Volume']-df['BuyVolume']
            #Average from Open and Close values, used for Volume Profile
            df['PriceAverage']=(df['Open']+df['Close'])/2
            self.df = df
        else:
            self.df = pd.DataFrame()
    
    #EMA of last n periods for Close column
    # df dataframe with column Close
    def ema(self, df, n, sma):
        alpha=2/(n+1)
        ema=np.nan
        lastema=sma
        if 500 >= len(df) >= 2*n+1 > 0 and 'Close' in df.columns:
            for i in range(n):
                ema=alpha*df.loc[len(df['Close'])-n+i,'Close']+(1-alpha)*lastema
                lastema=ema
        return ema
    
    #Add EMA of n periods column
    # df dataframe with column Close
    def addema(self,df,n):
        ema_list=[]
        for i in df.index.values:
            df_slice=df[0:i+1]
            sma=self.sma(df_slice[0:len(df_slice)-n],n)
            ema_list.append(self.ema(df_slice,n,sma))
        self.df['ema'+str(n)]=ema_list
    
    #Simple Media Average of last n periods for Close column
    # df dataframe with column Close
    def sma(self, df, n):
        if 500 >= len(df) >= n > 0 and 'Close' in df.columns:
            return df['Close'][len(df['Close'])-n:len(df['Close'])].mean()
        else:
            return np.nan
        
    #Add SMA of n periods column
    # df dataframe with column Close
    def addsma(self, df, n):
        sma_list=[]
        for i in df.index.values:
            df_slice=df[0:i+1]
            sma_list.append(self.sma(df_slice,n))
        self.df['sma'+str(n)]=sma_list
    
    #RSI of n periods
    # df dataframe with column Close
    def rsi(self, df, n):
        if 500 >= len(df) >= 2*n+1 > 0 and 'Close' in df.columns:
            #RMA for avgain and avloss
            avgain=0
            avloss=0
            alpha=(1.0/n)
            gainlist=[]
            losslist=[]
            for i in range(n,0,-1):                
                closedelta=df.loc[len(df)-n-i,'Close']-df.loc[len(df)-n-i-1,'Close']
                if closedelta > 0:
                    gainlist.append(closedelta)
                else:
                    losslist.append(abs(closedelta))
            avgain=np.array(gainlist).sum()/n
            avloss=np.array(losslist).sum()/n
            for i in range(n,0,-1):
                closedelta=df.loc[len(df)-i,'Close']-df.loc[len(df)-i-1,'Close']
                if closedelta > 0:
                    avgain=closedelta*alpha+(1-alpha)*avgain
                    avloss=(1-alpha)*avloss
                else:
                    avloss=abs(closedelta)*alpha+(1-alpha)*avloss
                    avgain=(1-alpha)*avgain                                
            rs=avgain/avloss
            rsi=100-(100/(1+rs))
            return rsi
        else:
            return np.nan
    
    #Add RSI of 14 periods column
    # df dataframe with column Close    
    def addrsi(self, df):
        rsi_list=[]
        n=14
        for i in df.index.values:
            df_slice=df[0:i+1]
            rsi_list.append(self.rsi(df_slice,n))
        self.df['rsi'+str(n)]=rsi_list

    #MACD
    # df dataframe with column Close
    def macd(self, df):
        if 500 >= len(df) >= 2*26+17+1 > 0 and 'Close' in df.columns:
            macd_list=[]
            for i in range(0,18):
                firstsma12=self.sma(df[0:len(df)-17+i-12],12)
                firstsma26=self.sma(df[0:len(df)-17+i-26],26)
                macd_list.append(self.ema(df[0:len(df)-17+i],12,firstsma12)-self.ema(df[0:len(df)-17+i],26,firstsma26))
            signal=self.emaoflist(macd_list[9:18],self.smaoflist(macd_list[0:9]))
            hist=macd_list[-1]-signal
            return macd_list[-1],signal,hist
        else:
            return np.nan,np.nan,np.nan
    
    #Add macd,signal and histogram columns
    # df dataframe with column Close
    def addmacd(self, df):
        macd_list=[]
        signal_list=[]
        hist_list=[]
        for i in df.index.values:
            df_slice=df[0:i+1]
            macd,signal,hist=self.macd(df_slice)
            macd_list.append(macd)
            signal_list.append(signal)
            hist_list.append(hist)
        self.df['macd']=macd_list
        self.df['signal']=signal_list
        self.df['histogram']=hist_list
    
    #Calculate simple media average of a list
    def smaoflist(self,list):
        n=len(list)
        sma=0
        for i in list:
            sma=sma+i
        sma=sma/n
        return sma
    
    #Calculate exponential media average of a list
    # sma is simple media average of last n values before the initial value in list
    def emaoflist(self,list, sma):
        n=len(list)
        lastema=sma
        ema=0
        alpha = 2 / (n + 1)
        for i in list:
            ema=(1-alpha)*lastema+alpha*i
            lastema=ema
        return ema
    
    def di(self,df):
        if 500 >= len(df) >= 2*14+1 > 0 and 'Close' in df.columns and 'High' in df.columns and 'Low' in df.columns:
            upDMlist=[]
            downDMlist=[]
            trlist=[]
            upDIlist=[]
            downDIlist=[]            
            for i in range(0,28):
                upDM=df.loc[len(df)-28+i,'High']-df.loc[len(df)-28+i-1,'High']
                downDM=df.loc[len(df)-28+i-1,'Low']-df.loc[len(df)-28+i,'Low']
                if not (upDM > 0 and upDM > downDM):
                    upDM=0
                if not (downDM > 0 and downDM > upDM):
                    downDM=0
                upDMlist.append(upDM)
                downDMlist.append(downDM)
                tr=max(df.loc[len(df)-28+i,'High']-df.loc[len(df)-28+i,'Low'], abs(df.loc[len(df)-28+i,'High']-df.loc[len(df)-28+i-1,'Close']), abs(df.loc[len(df)-28+i,'Low']-df.loc[len(df)-28+i-1,'Close']))
                trlist.append(tr)
            atrsma=self.smaoflist(trlist[0:14])
            atr=self.emaoflist(trlist[14:28],atrsma)
            sma=self.smaoflist(upDMlist[0:14])
            ema=self.emaoflist(upDMlist[14:28],sma)
            upDI=100*ema/atr
            sma=self.smaoflist(downDMlist[0:14])
            ema=self.emaoflist(downDMlist[14:28],sma)
            downDI=100*ema/atr
            return upDI,downDI
        else:
            return 0,0
    
    def adx(self,df):
        if 500 >= len(df) >= 2*14+1 > 0 and 'Close' in df.columns and 'High' in df.columns and 'Low' in df.columns:
            adxlist=[]
            for i in range(0,28):
                upDI,downDI=self.di(df[0:len(df)-28+i+1])
                if upDI+downDI == 0:
                    upDI=downDI=0.5
                adxlist.append(abs((upDI-downDI)/(upDI+downDI)))
            sma=self.smaoflist(adxlist[0:14])
            ema=self.emaoflist(adxlist[14:28],sma)
            adx=100*ema
            return upDI,downDI,adx
        else:
            return np.nan,np.nan,np.nan
    
    def addadx(self,df):
        upDI_list=[]
        downDI_list=[]
        adx_list=[]
        for i in df.index.values:
            df_slice=df[0:i+1]
            upDI,downDI,adx=self.adx(df_slice)
            upDI_list.append(upDI)
            downDI_list.append(downDI)
            adx_list.append(adx)
        self.df['upDI']=upDI_list
        self.df['downDI']=downDI_list
        self.df['adx']=adx_list
