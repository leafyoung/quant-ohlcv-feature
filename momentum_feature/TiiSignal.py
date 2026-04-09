import numpy as np
import pandas as pd


# ===== function: zscore normalization
def scale_zscore(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).mean()
          ) / pd.Series(_s).rolling(_n, min_periods=1).std()
    return pd.Series(_s)


def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # ******************** TII ********************
    # N1=40
    # M=[N1/2]+1
    # N2=9
    # CLOSE_MA=MA(CLOSE,N1)
    # DEV=CLOSE-CLOSE_MA
    # DEVPOS=IF(DEV>0,DEV,0)
    # DEVNEG=IF(DEV<0,-DEV,0)
    # SUMPOS=SUM(DEVPOS,M)
    # SUMNEG=SUM(DEVNEG,M)
    # TII=100*SUMPOS/(SUMPOS+SUMNEG)
    # TII_SIGNAL=EMA(TII,N2)
    # TII is calculated the same way as RSI, but replaces the two-day price change with the difference between price and moving average.
    # TII can be used to reflect the price trend and trend strength. Generally, TII>80 (<20) indicates a strong uptrend (downtrend).
    # There are several ways to generate trading signals with TII: cross above 20 to buy, cross below 80 to sell (as a reversal indicator); cross above 50 to buy, cross below 50 to sell;
    # cross above signal line to buy, cross below signal line to sell. If TII crosses above TII_SIGNAL, a buy signal is generated; if TII crosses below TII_SIGNAL, a sell signal is generated.
    close_ma = df['close'].rolling(n, min_periods=1).mean()
    dev = df['close'] - close_ma
    devpos = np.where(dev > 0, dev, 0)
    devneg = np.where(dev < 0, -dev, 0)
    sumpos = pd.Series(devpos).rolling(int(1 + n / 2), min_periods=1).sum()
    sumneg = pd.Series(devneg).rolling(int(1 + n / 2), min_periods=1).sum()

    tii = 100 * sumpos / (sumpos + sumneg)
    tii_signal = pd.Series(tii).ewm(span=int(n / 2), adjust=False, min_periods=1).mean()
    df[factor_name] = scale_zscore(tii_signal, n)

    return df
