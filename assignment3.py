# -*- coding: utf-8 -*-
"""Assignment3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Cb3CLlvMLKeLdMwd-b1RVW54JTHAGgu2
"""

!pip install yfinance
import yfinance as yf
import pandas as pd

def tradesig(close, open, high, low, close1, close2):
    tradesignal = 0
    if (close - open) / (high - low) > 0.9:
        tradesignal = 1
    elif (open - close) / (high - low) > 0.9:
        tradesignal = -1
    elif close2 < close1 < close:
        if abs(close - open) / (high - low) < 0.1:
            tradesignal = -1
        if (open - low) / (close - open) > 2 and (open - low) / (high - close) > 5:
            tradesignal = -1
    elif close2 > close1 > close:
        if abs(close - open) / (high - low) < 0.1:
            tradesignal = 1
        if (close-open)==0 or (high-close)==0:
            tradesignal =  1
        elif (open - low) / (close - open) > 2 and (open - low) / (high - close) > 5:
            tradesignal = 1
    return tradesignal

df = yf.download('AAPL', start='2018-01-01', end='2023-01-01')

tradeduration = 0
capital = 100000
invest = 0
x = 0
stoploss = 0
buyidx = []
sellidx = []
returns = []
tradurations=[]
maxdraw=[]
trough=0
peak=0
totpeak=df['Close'][0]
tottrough=df['Close'][0]
buy_price = 0
invested = False

for i in range(2, len(df) - 1):
    if tradesig(df['Close'][i], df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i - 1], df['Close'][i - 2]) == 1:
        if x == 0:
            invest = capital
            capital = 0
            buy_price = df['Close'][i]
            trough=df['Close'][i]
            peak=df['Close'][i]
            invested = True
            x = invest / df['Close'][i]
            stoploss = 0.95 * df['Close'][i]
            buyidx.append(i)
            if df['Close'][i]<tottrough:
             tottrough=df['Close'][i]
            elif df['Close'][i]>totpeak:
             totpeak=df['Close'][i]


    elif tradesig(df['Close'][i], df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i - 1], df['Close'][i - 2]) == -1 and invested == True:
        capital += x * df['Close'][i]
        if df['Close'][i]<trough:
         trough=df['Close'][i]
        elif df['Close'][i]>peak:
         peak=df['Close'][i]
        if df['Close'][i]<tottrough:
         tottrough=df['Close'][i]
        elif df['Close'][i]>totpeak:
         totpeak=df['Close'][i]
        trade_duration = i - buyidx[-1]
        tradurations.append(trade_duration)
        invested = False
        sellidx.append(i)
        returns.append(x * df['Close'][i] - x * buy_price)
        x = 0
        maxdraw_trade=(peak-trough)/peak*100
        maxdraw.append(maxdraw_trade)

    elif invested == True and df['Close'][i] < stoploss:
        capital += x * stoploss

        trade_duration = i - buyidx[-1]
        tradurations.append(trade_duration)
        invested = False
        sellidx.append(i)
        trade_return = x * stoploss - x * buy_price
        returns.append(trade_return)
        x = 0
        maxdraw_trade=(peak-stoploss)/peak*100
        maxdraw.append(maxdraw_trade)
    else:
       if df['Close'][i]<trough:
        trough=df['Close'][i]
       elif df['Close'][i]>peak:
        peak=df['Close'][i]
       if df['Close'][i]<tottrough:
        tottrough=df['Close'][i]
       elif df['Close'][i]>totpeak:
        totpeak=df['Close'][i]


trade_data = pd.DataFrame({
    'Entry Index': buyidx,
    'Exit Index': sellidx,
    'Returns': returns,
    'Trade Duration': tradurations,
    'Max Drawdown(in %)': maxdraw

})

profitperc=(capital-100000)/100000*100
print(trade_data)
print("Return Percentage ",profitperc,"%")
print("Final Capital ",capital)
print("Largest Drawdown in the complete trade ",(totpeak-tottrough)/totpeak*100,"%")