from pandas_datareader import data as pdr
import yfinance
import pandas as pd


data = pdr.get_data_yahoo("^NSEI", start="2021-01-01", end="2021-03-01")
data = pd.DataFrame(data)

# https://blog.quantinsti.com/build-technical-indicators-in-python/
# CCI = (TP - SMA 20 OF TP) / (0.15 * MEAN DEVIATION)
# where,
# Typical Price (TP) = (HIGH + LOW + CLOSE) / 3
# SMA 20 of TP = Typical Price / 20
# Mean Deviation = Absolute values of Typical Price / 20
def CCI(df, ndays): 
        TP = (data['High'] + data['Low'] + data['Close']) / 3
        sma = TP.rolling(ndays).mean()
        mad = TP.rolling(ndays).apply(lambda x: pd.Series(x).mad())
        cci = (TP - sma) / (0.015 * mad) 
        return cci

def NZ(data):
        ret_val = (0 if (data is None) else data)
        return ret_val


prev_e1 = None
prev_e2 = None
prev_e3 = None
prev_e4 = None
prev_e5 = None
prev_e6 = None

while (True):
        CCI_Period = 14							# CCI_Period = input(14, minval=1)
        T3_Period = 5							# T3_Period = input(5, minval=1)
        b = 0.618							# b = input(0.618)
        								# hline(0, color=purple, linestyle=line)
        xPrice = data['Close']						# xPrice = close
        b2 = b*b							# b2 = b*b
        b3 = b2*b							# b3 = b2*b
        c1 = -b3							# c1 = -b3
        c2 = (3*(b2 + b3))						# c2 = (3*(b2 + b3))
        c3 = -3*(2*b2 + b + b3)                                         # c3 = -3*(2*b2 + b + b3)
        c4 = (1 + 3*b + b3 + 3*b2)                                      # c4 = (1 + 3*b + b3 + 3*b2)
        nn = 1 if (T3_Period < 1) else T3_Period                        # nn = iff(T3_Period < 1, 1, T3_Period)
        nr = 1 + 0.5*(nn - 1)                                           # nr = 1 + 0.5*(nn - 1)
        w1 = 2 / (nr + 1)						# w1 = 2 / (nr + 1)
        w2 = 1 - w1							# w2 = 1 - w1
        xcci = CCI(xPrice, CCI_Period)                                  # xcci = cci(xPrice, CCI_Period)
        e1 = w1*xcci + w2*NZ(prev_e1)                                   # e1 = w1*xcci + w2*nz(e1[1])
        e2 = w1*e1 + w2*NZ(prev_e2)                                     # e2 = w1*e1 + w2*nz(e2[1])
        e3 = w1*e2 + w2*NZ(prev_e3)                                     # e3 = w1*e2 + w2*nz(e3[1])
        e4 = w1*e3 + w2*NZ(prev_e4)                                     # e4 = w1*e3 + w2*nz(e4[1])
        e5 = w1*e4 + w2*NZ(prev_e5)                                     # e5 = w1*e4 + w2*nz(e5[1])
        e6 = w1*e5 + w2*NZ(prev_e6)                                     # e6 = w1*e5 + w2*nz(e6[1])
        xccir = c1*e6 + c2*e5 + c3*e4 + c4*e3                           # xccir = c1*e6 + c2*e5 + c3*e4 + c4*e3

        print(xccir)

        prev_e1 = e1
        prev_e2 = e2
        prev_e3 = e3
        prev_e4 = e4
        prev_e5 = e5
        prev_e6 = e6

        control = input("'y' key for continue, other key for exit: ")
        if (control != 'y'):
                break
