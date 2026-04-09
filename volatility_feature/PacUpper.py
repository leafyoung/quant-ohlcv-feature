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

    # ******************** Pac ********************
    # N1=20
    # N2=20
    # UPPER=SMA(HIGH,N1,1)
    # LOWER=SMA(LOW,N2,1)
    # Construct a price channel using moving averages of high and low prices. Go long if price breaks above the upper band; go short if it breaks below the lower band.
    upper = df['high'].ewm(alpha=1 / n, adjust=False).mean()
    df[factor_name] = scale_01(upper, n)

    return df
