#!/usr/bin/env python
"""
Technical Analisys Library for Binance candles
Version 20191230
"""
# importing libraries
import requests

def klines(symbol, interval):
    #Input parameters
    symbol=symbol
    interval=interval

    #url_base='https://api.binance.com/api/v1/klines?symbol=BTCUSDT&interval=5m'
    url_base='https://api.binance.com/api/v1/klines'
    
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'symbol':symbol, 'interval':interval}
    myheaders = {}
    # sending get request and saving the response as response object
    try:
        myrequest = requests.get(url = url_base, headers = myheaders, params = PARAMS)
        #print(myrequest.status_code)
        # extracting data in json format
        return myrequest.json()
    except:
        return(['klines API error'])

def rsi(symbol, interval):
    data = klines(symbol,interval)
    #print data
    #RSI calculation
    counter=0
    lastclose=0
    delta=0
    gain=0
    avgain=0
    loss=0
    avloss=0
    RS=0
    RSI=0
    p=14
    #MMV
    a=(1.0/p)
    #EMA
    #a=2.0/(1+p) 
    
    for i in data:
            #....
            if counter==0:
                    lastclose=float(i[4])
            elif counter >= 1 and counter <= 13:
                    delta=float(i[4])-lastclose
                    if delta <= 0: loss=loss+abs(delta)
                    else: gain=gain+abs(delta)
                    lastclose=float(i[4])
            elif counter==14:
                    avloss=loss/14
                    avgain=gain/14
                    #print str(avloss)+' '+str(avgain)
                    RS=avgain/avloss
                    RSI=100-100/(1+RS)
                    delta=float(i[4])-lastclose
                    if delta <= 0:
                            avloss=abs(delta)*a+(1-a)*avloss
                            avgain=0*a+(1-a)*avgain
                    else:
                            avgain=abs(delta)*a+(1-a)*avgain
                            avloss=0*a+(1-a)*avloss
                    lastclose=float(i[4])
                    #print RSI
            else:
                    #print str(delta)+' '+str(avloss)+' '+str(avgain)
                    RS=avgain/avloss
                    RSI=100-100/(1+RS)
                    delta=float(i[4])-lastclose
                    if delta <= 0:
                            avloss=abs(delta)*a+(1-a)*avloss
                            avgain=0*a+(1-a)*avgain
                    else:
                            avgain=abs(delta)*a+(1-a)*avgain
                            avloss=0*a+(1-a)*avloss
                    lastclose=float(i[4])
                    #print RSI
            counter+=1
    RS=avgain/avloss
    RSI=100-100/(1+RS)
    return RSI
	

def rsi_klines(klines):
    data = klines
    #print data
    #RSI calculation
    counter=0
    lastclose=0
    delta=0
    gain=0
    avgain=0
    loss=0
    avloss=0
    RS=0
    RSI=0
    p=14
    #MMV
    a=(1.0/p)
    #EMA
    #a=2.0/(1+p) 
    
    for i in data:
            #....
            if counter==0:
                    lastclose=float(i[4])
            elif counter >= 1 and counter <= 13:
                    delta=float(i[4])-lastclose
                    if delta <= 0: loss=loss+abs(delta)
                    else: gain=gain+abs(delta)
                    lastclose=float(i[4])
            elif counter==14:
                    avloss=loss/14
                    avgain=gain/14
                    #print str(avloss)+' '+str(avgain)
                    RS=avgain/avloss
                    RSI=100-100/(1+RS)
                    delta=float(i[4])-lastclose
                    if delta <= 0:
                            avloss=abs(delta)*a+(1-a)*avloss
                            avgain=0*a+(1-a)*avgain
                    else:
                            avgain=abs(delta)*a+(1-a)*avgain
                            avloss=0*a+(1-a)*avloss
                    lastclose=float(i[4])
                    #print RSI
            else:
                    #print str(delta)+' '+str(avloss)+' '+str(avgain)
                    RS=avgain/avloss
                    RSI=100-100/(1+RS)
                    delta=float(i[4])-lastclose
                    if delta <= 0:
                            avloss=abs(delta)*a+(1-a)*avloss
                            avgain=0*a+(1-a)*avgain
                    else:
                            avgain=abs(delta)*a+(1-a)*avgain
                            avloss=0*a+(1-a)*avloss
                    lastclose=float(i[4])
                    #print RSI
            counter+=1
    RS=avgain/avloss
    RSI=100-100/(1+RS)
    return RSI
	
def linreg(X, Y):
    N=len(X)
    Sx=Sy=Sxx=Syy=Sxy=0.0
    for x,y in zip(X,Y):
        Sx=Sx+x
        Sy=Sy+y
        Sxx=Sxx+x*x
        Syy=Syy+y*y
        Sxy=Sxy+x*y
    det=Sxx*N-Sx*Sx
    return (Sxy*N-Sy*Sx)/det, (Sxx*Sy-Sx*Sxy)/det

def closePriceList(klines):
    index=0
    Y=[]
    X=[]
    for i in klines:
        Y.append(float(i[4]))
        X.append(index)
        index=index+1
    return X,Y

def trendIndex(klines5m,klines15m):
    index=0
    #klines1m=klines(symbol,'1m')
    #klines5m=klines(symbol,'5m')
    #klines15m=klines(symbol,'15m')
    #klines1h=klines(symbol,'1h')
    #klines4h=klines(symbol,'4h')
    #klines1d=klines(symbol,'1d')
    #len(klines1d)=484
    #m1m,Y=closePriceList(klines1m[495:])
    #print(linreg(X,Y))
    X,Y=closePriceList(klines5m[488:])
    #print(linreg(X,Y))
    m5m,b=linreg(X,Y)
    X,Y=closePriceList(klines15m[488:])
    #print(linreg(X,Y))
    m15m, b = linreg(X,Y)
    #X,Y=closePriceList(klines1h[495:])
    #print(linreg(X,Y))
    #m1h, b = linreg(X,Y)
    #X,Y=closePriceList(klines4h[495:])
    #print(linreg(X,Y))
    #m4h,b=linreg(X,Y)
    #X,Y=closePriceList(klines1d[479:])
    #print(linreg(X,Y))
    #m1d,b=linreg(X,Y)
    #Evaluation
    if m5m<0 and rsi_klines(klines5m)>33:
        #print('5m, downtrend, not oversold, not long')
        index = index + 0
    elif m5m<0 and rsi_klines(klines5m)<33:
        #print('5m, downtrend, oversold, possible long')
        index = index + 1
    else:
        #print('5m, uptrend, possible long')
        index = index + 2
    if m15m<0 and rsi_klines(klines5m)>33:
        #print('15m, downtrend, not oversold, not long')
        index = index + 0
    elif m15m<0 and rsi_klines(klines5m)<33:
        #print('15m, downtrend, oversold, possible long')
        index = index + 2
    else:
        #print('15m, uptrend, possible long')
        index = index + 2
    if index>=3: return 'uptrend'
    else: return 'downtrend'

def minClose(klines,n):
    index=499
    minprice=klines[index][4]
    for i in range(499,499-n+1,-1):
        if klines[i-1][4]<minprice:
            minprice=klines[i-1][4]
            index=i-1
    return index

def maxClose(klines,n):
    index=499
    maxprice=klines[index][4]
    for i in range(499,499-n+1,-1):
        if klines[i-1][4]>maxprice:
            maxprice=klines[i-1][4]
            index=i-1
    return index
	

def minOfList(list):
    if len(list)==1: return list[0]
    else:
        return min(list[0], minOfList(list[1:]))

def maxOfList(list):
    if len(list)==1: return list[0]
    else:
        return max(list[0], maxOfList(list[1:]))

def stochRSI(klines):
    k=0
    d=0
    rsiList=[]
    for i in range(0,18):
        n=len(klines)
        #print(i,len(klines[:n-i]))
        rsi=rsi_klines(klines[:n-i])
        rsiList.append(rsi)
        #print(rsi)
        #rsi = rsi_klines(klines)
        #print(rsi)
    #print(rsiList)
    #k499
    rsiL=minOfList(rsiList[:14])
    rsiH=maxOfList(rsiList[:14])
    #print(rsiL,rsiH, rsiList[:14])
    k499=(rsiList[0]-rsiL)/(rsiH-rsiL)*100
    #k498
    rsiL=minOfList(rsiList[1:15])
    rsiH=maxOfList(rsiList[1:15])
    #print(rsiL,rsiH, rsiList[1:15])
    k498=(rsiList[1]-rsiL)/(rsiH-rsiL)*100
    #k497
    rsiL = minOfList(rsiList[2:16])
    rsiH = maxOfList(rsiList[2:16])
    #print(rsiL, rsiH, rsiList[2:16])
    k497 = (rsiList[2] - rsiL) / (rsiH - rsiL) * 100
    #k496
    rsiL = minOfList(rsiList[3:17])
    rsiH = maxOfList(rsiList[3:17])
    #print(rsiL, rsiH, rsiList[3:17])
    k496 = (rsiList[3] - rsiL) / (rsiH - rsiL) * 100
    #495
    rsiL = minOfList(rsiList[4:18])
    rsiH = maxOfList(rsiList[4:18])
    #print(rsiL, rsiH, rsiList[4:18])
    k495 = (rsiList[4] - rsiL) / (rsiH - rsiL) * 100
    sma_k499 = (k499 + k498 + k497) / 3
    sma_k498 = (k498 + k497 + k496) / 3
    sma_k497 = (k497 + k496 + k495) / 3
    k=sma_k499
    d=(sma_k499+sma_k498+sma_k497)/3
    return k,d

def sma(klines):
    n=len(klines)
    #print(n)
    sma=0
    for i in klines:
        sma=sma+float(i[4])
    sma=sma/n
    return sma

def ema(klines, sma):
    n=len(klines)
    #print(n)
    last_ema=sma
    ema=0
    mul = 2 / (n + 1)
    for i in klines:
        ema=(float(i[4])-last_ema)*mul+last_ema
        last_ema=ema
    return ema

def indexOfMaxInList(list):
    n=len(list)
    index=0
    max=list[0]	
    for i in range(0,n-1):
	    if max<=list[i+1]:
             index=i+1
             max=list[i+1]
    return index

def indexOfMinInList(list):
    n=len(list)
    index=0
    min=list[0]	
    for i in range(0,n-1):
	    if min>=list[i+1]:
             index=i+1
             min=list[i+1]
    return index	
	
def macd(klines):
    n=len(klines)
    macd=0
    signal=0
    macd_list=[]
    indexofmaxmacd=0
    indexofminmacd=0
    for i in range(0,18):
        #SMA 26-periodos (473-448)
        #sma473=sma(klines[448-i:474-i])
        sma473=sma(klines[n-26*2-i:n-26-i])
        #EMA 26-periods (499-474)
        #ema26=ema(klines[474-i:500-i],sma473)
        ema26=ema(klines[n-26-i:n-i],sma473)
        #SMA 12-periods (487-476)
        #sma487=sma(klines[476-i:488-i])
        sma487=sma(klines[n-12*2-i:n-12-i])
        #EMA 12-periods (499-488)
        #ema12 = ema(klines[488-i:500-i], sma487)
        ema12 = ema(klines[n-12-i:n-i], sma487)
        #macd=EMA12-EMA26
        macd=ema12-ema26
        macd_list.append(macd)
    #indexofmaxmacd=499-indexOfMaxInList(macd_list[0:7])
    #indexofminmacd=499-indexOfMinInList(macd_list[0:7])
    indexofmaxmacd=indexOfMaxInList(macd_list[0:7])
    indexofminmacd=indexOfMinInList(macd_list[0:7])
    #signal=EMA9(macd) (499-491)
    #SMA9(macd) (490-482)
    sma490=0
    for i in macd_list[9:18]:
        sma490=sma490+i
    sma490=sma490/9
    #EMA9(macd) (499-491)
    mul=2/(9+1)
    last_signal=sma490
    for i in range(0,9):
        signal = (macd_list[8-i] - last_signal) * mul + last_signal
        last_signal = signal
    return macd_list[0], signal, indexofmaxmacd, indexofminmacd

def smaoflist(list):
    n=len(list)
    #print(n)
    sma=0
    for i in list:
        sma=sma+i
    sma=sma/n
    return sma

def emaoflist(list, sma):
    n=len(list)
    #print(n)
    last_ema=sma
    ema=0
    mul = 2 / (n + 1)
    for i in list:
        ema=(i-last_ema)*mul+last_ema
        last_ema=ema
    return ema

def di(klines):
    n=len(klines)-1
    upDMlist=[]
    downDMlist=[]
    trlist=[]
    upDIlist=[]
    downDIlist=[]
    for i in range(0,56):
        upDM=float(klines[n-55+i][2])-float(klines[n-56+i][2])
        downDM=downDM=float(klines[n-55+i][3])-float(klines[n-56+i][3])
        if upDM > 0 and upDM > downDM:
            upDM=upDM
        else: upDM=0
        if downDM > 0 and downDM > upDM:
            downDM=downDM
        else: downDM=0
        upDMlist.append(upDM)
        downDMlist.append(downDM)
        tr=max(float(klines[n-55+i][2])-float(klines[n-55+i][3]), abs(float(klines[n-55+i][2])-float(klines[n-56+i][4])), abs(float(klines[n-55+i][3])-float(klines[n-56+i][4])))
        trlist.append(tr)
    atrsma=smaoflist(trlist[28:42])
    atr=emaoflist(trlist[42:56],atrsma)
    sma=smaoflist(upDMlist[28:42])
    ema=emaoflist(upDMlist[42:56],sma)
    upDI=100*ema/atr
    sma=smaoflist(downDMlist[28:42])
    ema=emaoflist(downDMlist[42:56],sma)
    downDI=100*ema/atr
    return upDI,downDI

def adx(klines):
    adxlist=[]
    n=len(klines)
    for i in range(0,28):
        upDI,downDI=di(klines[0:n-27+i])
        adxlist.append(abs((upDI-downDI)/(upDI+downDI)))
    sma=smaoflist(adxlist[0:14])
    ema=emaoflist(adxlist[14:28],sma)
    adx=100*ema
    return upDI,downDI,adx

