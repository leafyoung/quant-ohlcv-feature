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
    # Ma indicator (Moving Average, 0-1 normalized)
    # Formula: MA = MA(CLOSE, N); result = scale_01(MA, N)
    # Computes the rolling mean of close price and normalizes to [0,1] within its rolling range.
    # Values near 1 indicate MA is near its recent high; values near 0 indicate near its recent low.
    s = df['close'].rolling(n, min_periods=1).mean()
    df[factor_name] = scale_01(s, n)

    return df
