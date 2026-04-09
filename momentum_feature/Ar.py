import pandas as pd


def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # Ar indicator (Atmosphere Ratio)
    # Formula: AR = 100 * SUM(HIGH - OPEN, N) / SUM(OPEN - LOW, N)
    # Measures buying power relative to selling power based on the candle's open position.
    # AR > 100 indicates buyers dominated (close above open); AR < 100 indicates sellers dominated.
    v1 = (df['high'] - df['open']).rolling(n, min_periods=1).sum()
    v2 = (df['open'] - df['low']).rolling(n, min_periods=1).sum()
    _ar = 100 * v1 / v2
    df[factor_name] = pd.Series(_ar)

    return df
