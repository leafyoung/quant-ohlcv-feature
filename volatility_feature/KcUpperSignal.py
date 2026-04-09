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
    # ******************** KC ********************
    # N=14
    # TR=MAX(ABS(HIGH-LOW),ABS(HIGH-REF(CLOSE,1)),ABS(REF(CLOSE,1)-REF(LOW,1)))
    # ATR=MA(TR,N)
    # Middle=EMA(CLOSE,20)
    # UPPER=MIDDLE+2*ATR
    # LOWER=MIDDLE-2*ATR
    # The KC indicator (Keltner Channel) is similar to Bollinger Bands, both using the price moving average to construct the middle band; the difference is in the method of representing amplitude.
    # Here ATR is used as the amplitude to construct upper and lower bands. Price breaking through the upper band can be seen as a new uptrend, buy; breaking through the lower band as a new downtrend, sell.
    tmp1_s = df['high'] - df['low']
    tmp2_s = (df['high'] - df['close'].shift(1)).abs()
    tmp3_s = (df['low'] - df['close'].shift(1)).abs()
    tr = np.max(np.array([tmp1_s, tmp2_s, tmp3_s]), axis=0)  # take maximum of three series

    atr = pd.Series(tr).rolling(n, min_periods=1).mean()
    middle = df['close'].ewm(span=n, adjust=False, min_periods=1).mean()

    s = df['close'] - middle - 2 * atr
    df[factor_name] = scale_01(s, n)

    return df
