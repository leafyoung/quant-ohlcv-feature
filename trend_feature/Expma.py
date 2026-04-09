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

    # ******************** Expma ********************
    # N1=12
    # N2=50
    # EMA1=EMA(CLOSE,N1)
    # EMA2=EMA(CLOSE,N2)
    # Exponential Moving Average is an improved version of the Simple Moving Average, designed to reduce the lag problem.
    ema1 = df['close'].ewm(span=n, min_periods=1).mean()
    ema2 = df['close'].ewm(span=(4 * n), min_periods=1).mean()

    s = ema1 - ema2
    df[factor_name] = scale_01(s, n)

    return df
