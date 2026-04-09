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

    # Hullma indicator
    """
    N=20,80
    X=2*EMA(CLOSE,[N/2])-EMA(CLOSE,N)
    Hullma=EMA(X,[√N])
    Hullma is a type of moving average with lower lag compared to ordinary moving averages. We use
    the short-term moving average crossing above/below the long-term moving average to generate buy/sell signals.
    """
    _x = 2 * df['close'].ewm(span=int(n / 2), adjust=False, min_periods=1).mean() - df['close'].ewm(
        span=n, adjust=False, min_periods=1).mean()
    hullma = _x.ewm(span=int(np.sqrt(n)), adjust=False, min_periods=1).mean()

    s = _x - hullma
    df[factor_name] = scale_01(s, n)

    return df
