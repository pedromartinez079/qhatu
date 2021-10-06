# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 09:37:53 2019

@author: Dropex
"""

import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import libTA as libTA
import time

def graphs(symbol,interval):
    # interval 1m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d 1w 1M
    symbol = symbol
    interval = interval    
    r = requests.get('https://api.binance.com/api/v3/klines?symbol='+symbol+'&interval='+interval)
    data = r.json()
    n = len(data)
    #print(n)
    #print(data[n-1][4])
    #print(libTA.adx(data))
    #print(time.strftime("%d%b%Y %H:%M", time.localtime()))
    
    x=[]
    y0=[]
    y3=[]
    y8=[]
    y21=[]
    y50=[]
    y100=[]
    y200=[]
    y300=[]
    rsi=[]
    highrsi=[]
    lowrsi=[]
    macd=[]
    signal=[]
    macd0=[]
    k=[]
    d=[]
    highstoch=[]
    lowstoch=[]
    upDI=[]
    downDI=[]
    adx=[]
    keylevel=[]
    klines_bulk=[]
    klines=[]
    
    for i in range(0,200):
        klines_bulk.append([i])
    
    for i in range(0,201):
        if interval == '1d' : 
            unitoftime = 24*60*60
        elif interval == '1w' : unitoftime = 7*24*60*60
        elif interval == '3d' : unitoftime = 3*24*60*60
        elif interval == '12h' : unitoftime = 12*60*60
        elif interval == '6h' : unitoftime = 6*60*60
        elif interval == '4h' : unitoftime = 4*60*60
        elif interval == '1h' : unitoftime = 1*60*60
        elif interval == '15m' : unitoftime = 15*60
        elif interval == '5m' : unitoftime = 5*60
        elif interval == '1m' : unitoftime = 1*60
        x.append(time.strftime("%d%b%Y %H:%M",time.localtime(time.time()-(199-i)*unitoftime)))
        if n-3-200+i >= 0 : sma3 = libTA.sma(data[n-3-200+i:n-200+i])
        else : sma3 = 0
        if n-8-200+i >= 0 : sma8 = libTA.sma(data[n-8-200+i:n-200+i])
        else : sma8 = 0
        if n-21-200+i >= 0 : sma21 = libTA.sma(data[n-21-200+i:n-200+i])
        else : sma21 = 0
        if n-50-200+i >= 0 : sma50 = libTA.sma(data[n-50-200+i:n-200+i])
        else : sma50 = 0
        if n-100-200+i >= 0 : sma100 = libTA.sma(data[n-100-200+i:n-200+i])
        else : sma100 = 0
        if n-200-200+i >= 0 : sma200 = libTA.sma(data[n-200-200+i:n-200+i])
        else : sma200 = 0
        if n-300-200+i >= 0 : sma300 = libTA.sma(data[n-300-200+i:n-200+i])
        else : sma300 = 0
        if n-200+i >= 15: rsi.append(libTA.rsi_klines(data[0:n-200+i]))
        else : rsi.append(0)
        highrsi.append(70)
        lowrsi.append(30)
        klines.extend(klines_bulk)
        klines.extend(data[0:300+i])
        if n >= 500: 
            m,s,maxindex,minindex = libTA.macd(klines[0+i:n+i])
            macd.append(m)
            signal.append(s)
        else :
            macd.append(0)
            signal.append(0)
        macd0.append(0)
        if n-200+i > 31 : ku,du = libTA.stochRSI(data[0:n-200+i])
        else : ku = du = 0
        k.append(ku)
        d.append(du)
        highstoch.append(80)
        lowstoch.append(20)
        if n-200+i > 56 : upDIu, downDIu, adxu = libTA.adx(data[0:n-200+i])
        else : upDIu = downDIu = adxu = 0
        upDI.append(upDIu)
        downDI.append(downDIu)
        adx.append(adxu)
        keylevel.append(23)
        if n >= 201: y0.append(float(data[n-201+i][4]))
        else : y0.append(0)
        #y3.append(sma3)
        y8.append(sma8)
        y21.append(sma21)
        y50.append(sma50)
        y100.append(sma100)
        y200.append(sma200)
        y300.append(sma300)
        klines=[]
        #print('3|%.2f 8|%.2f 21|%.2f 50|%.2f 100|%.2f 200|%.2f 300|%.2f' %(sma3,sma8,sma21,sma50,sma100,sma200,sma300))
    # 7SMA
    plt.plot(x,y0,label='Price',color='black')
    #plt.plot(x,y3,label='sma3')
    plt.plot(x,y8,label='sma8')
    plt.plot(x,y21,label='sma21')
    plt.plot(x,y50,label='sma50')
    plt.plot(x,y100,label='sma100')
    plt.plot(x,y200,label='sma200')
    plt.plot(x,y300,label='sma300')
    plt.xticks((x[0],x[19],x[39],x[59],x[79],x[99],x[119],x[139],x[159],x[179],x[199]), rotation=75)
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.xlabel('Time Unit') 
    plt.ylabel(symbol[0:3]+' Price') 
    plt.title('7 SMA '+interval) 
    plt.legend()
    plt.savefig('7sma.jpg')
    plt.show()
    # RSI
    plt.plot(x,rsi)
    plt.plot(x,highrsi, lowrsi, color='black')
    plt.xticks((x[0],x[19],x[39],x[59],x[79],x[99],x[119],x[139],x[159],x[179],x[199]), rotation=75)
    plt.xlabel('Time Unit') 
    plt.ylabel('RSI') 
    plt.title('RSI '+interval) 
    plt.savefig('rsi.jpg')
    plt.show()
    # MACD
    plt.plot(x,macd,signal)
    plt.plot(x,macd0,color='black')
    plt.xticks((x[0],x[19],x[39],x[59],x[79],x[99],x[119],x[139],x[159],x[179],x[199]), rotation=75)
    plt.xlabel('Time Unit') 
    plt.ylabel('Unit') 
    plt.title('MACD '+interval) 
    plt.savefig('macd.jpg')
    plt.show()
    # StochasticRSI
    plt.plot(x,k,d)
    plt.plot(x,highstoch, lowstoch,color='black')
    plt.xticks((x[0],x[19],x[39],x[59],x[79],x[99],x[119],x[139],x[159],x[179],x[199]), rotation=75)
    plt.xlabel('Time Unit') 
    plt.ylabel('Unit') 
    plt.title('StochasticRSI '+interval) 
    plt.savefig('stochasticRSI.jpg')
    plt.show()
    # ADX
    plt.plot(x,upDI,label='+DI',color='lightblue')
    plt.plot(x,downDI,label='-DI',color='lightgray')
    plt.plot(x,adx,label='ADX',color='orange')
    plt.plot(x,keylevel,label='KeyLevel',color='black')
    plt.xticks((x[0],x[19],x[39],x[59],x[79],x[99],x[119],x[139],x[159],x[179],x[199]), rotation=75)
    plt.xlabel('Time Unit') 
    plt.ylabel('Unit') 
    plt.title('DMI/ADX '+interval)
    plt.legend() 
    plt.savefig('adx.jpg')
    plt.show()

