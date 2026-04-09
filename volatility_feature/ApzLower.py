import pandas as pd


def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)


def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # ApzLower indicator
    """
    N=10
    M=20
    PARAM=2
    VOL=EMA(EMA(HIGH-LOW,N),N)
    UPPER=EMA(EMA(CLOSE,M),M)+PARAM*VOL
    LOWER= EMA(EMA(CLOSE,M),M)-PARAM*VOL
    ApzLower (Adaptive Price Zone) is similar to Bollinger Bands and the Keltner Channel:
    all are price channels built around a moving average based on price volatility.
    The difference lies in how volatility is measured: Bollinger Bands use the standard
    deviation of the close, the Keltner Channel uses the true range ATR, and ApzLower uses
    the N-day double exponential average of the high-low difference to measure price amplitude.
    """
    vol = (df['high'] - df['low']).ewm(span=n, adjust=False, min_periods=1).mean().ewm(
        span=n, adjust=False, min_periods=1).mean()
    upper = df['close'].ewm(span=int(2 * n), adjust=False, min_periods=1).mean().ewm(
        span=int(2 * n), adjust=False, min_periods=1).mean() + 2 * vol

    s = upper - 4 * vol
    df[factor_name] = scale_01(s, n)

    return df
