import numpy as np
import pandas as pd


eps = 1e-8


def signal(*args):
    # AtrUpper indicator (ATR-based upper band ratio vs MA)
    # Formula: ATR = EMA(TR, N).shift(1); LOWER_N2 = MIN(LOW, N/2)
    #          result = (LOWER_N2 + 3 * ATR) / MA(CLOSE, N)
    # Constructs an ATR-based upper channel using recent low plus 3×ATR, normalized by the MA.
    # Values above 1 indicate the upper band is significantly above the MA (wide channel / high volatility).
    df = args[0]
    n = args[1]
    factor_name = args[2]

    tr = np.max(np.array([
        (df['high'] - df['low']).abs(),
        (df['high'] - df['close'].shift(1)).abs(),
        (df['low'] - df['close'].shift(1)).abs()
    ]), axis=0)  # take the maximum of the three series
    atr = pd.Series(tr).ewm(alpha=1 / n, adjust=False).mean().shift(1)
    _low = df['low'].rolling(int(n / 2), min_periods=1).min()
    _ma = df['close'].rolling(n, min_periods=1).mean()
    df[factor_name] = (_low + 3 * atr) / (_ma + eps)

    return df
