import numpy as np
import pandas as pd


# ===== function: 0-1 normalization
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)


def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # ******************** FbUpperSignal indicator ********************
    # N=20
    # TR=MAX(HIGH-LOW,ABS(HIGH-REF(CLOSE,1)),ABS(LOW-REF(CLOSE,1)))
    # ATR=MA(TR,N)
    # MIDDLE=MA(CLOSE,N)
    # UPPER1=MIDDLE+1.618*ATR
    # UPPER2=MIDDLE+2.618*ATR
    # UPPER3=MIDDLE+4.236*ATR
    # LOWER1=MIDDLE-1.618*ATR
    # LOWER2=MIDDLE-2.618*ATR
    # LOWER3=MIDDLE-4.236*ATR
    # The FB indicator is similar to Bollinger Bands, both using the price moving average as the middle band, constructing upper and lower bands by floating a certain value above and below.
    # Unlike Bollinger Bands, Fibonacci Bands have three upper and three lower bands, obtained by adding/subtracting ATR multiplied by Fibonacci factors from the middle band.
    # When the close price breaks through one of the two higher upper bands, a buy signal is generated; when it breaks through one of the two lower bands, a sell signal is generated.
    tmp1_s = df['high'] - df['low']
    tmp2_s = (df['high'] - df['close'].shift(1)).abs()
    tmp3_s = (df['low'] - df['close'].shift(1)).abs()

    tr = np.max(np.array([tmp1_s, tmp2_s, tmp3_s]), axis=0)  # take maximum of three series

    atr = pd.Series(tr).rolling(n, min_periods=1).mean()
    middle = df['close'].rolling(n, min_periods=1).mean()

    s = df['close'] - middle - 1.618 * atr
    df[factor_name] = scale_01(s, n)

    return df
