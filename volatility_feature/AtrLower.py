import numpy as np
import pandas as pd


eps = 1e-8


def signal(*args):
    # AtrLower indicator (ATR lower band ratio vs MA)
    # Formula: ATR = MA(TR, N); MA = MA(CLOSE, N)
    #          LOWER = MA - ATR * 0.2 * N; result = LOWER / MA
    # Computes an ATR-based lower band scaled by window length, normalized as a ratio to MA.
    # Values below 1 indicate the lower band is significantly below the moving average (wide channel).
    df = args[0]
    n = args[1]
    factor_name = args[2]

    tr = np.max(np.array([
        df['high'] - df['low'],
        (df['high'] - df['close'].shift(1)).abs(),
        (df['low'] - df['close'].shift(1)).abs()
    ]), axis=0)
    atr = pd.Series(tr).rolling(n, min_periods=1).mean()
    _ma = df['close'].rolling(n, min_periods=1).mean()

    dn = _ma - atr * 0.2 * n
    df[factor_name] = dn / (_ma + eps)

    return df
