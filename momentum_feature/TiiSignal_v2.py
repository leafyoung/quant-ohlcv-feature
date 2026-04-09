import numpy as np
import pandas as pd


# ===== Function: 0-1 normalization
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
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
    # TII is calculated like RSI, but the price change between two consecutive days is replaced
    # with the deviation of price from its moving average. TII reflects price trend direction and strength.
    # Generally, TII > 80 indicates a strong uptrend, TII < 20 indicates a strong downtrend.
    # Several methods can be used to generate signals: cross above 20 to buy, cross below 80 to sell (reversal);
    # cross above 50 to buy, cross below 50 to sell; or cross above signal line to buy, cross below to sell.
    # A buy signal is generated when TII crosses above TII_SIGNAL; a sell signal when TII crosses below TII_SIGNAL.
    close_ma = df['close'].rolling(n, min_periods=1).mean()
    dev = df['close'] - close_ma
    devpos = np.where(dev > 0, dev, 0)
    devneg = np.where(dev < 0, -dev, 0)
    sumpos = pd.Series(devpos).rolling(int(1 + n / 2), min_periods=1).sum()
    sumneg = pd.Series(devneg).rolling(int(1 + n / 2), min_periods=1).sum()

    tii = 100 * sumpos / (sumpos + sumneg)
    tii_signal = pd.Series(tii).ewm(span=int(n / 2), adjust=False, min_periods=1).mean()
    tii_signal = tii - tii_signal
    df[factor_name] = scale_01(tii_signal, n)

    return df
