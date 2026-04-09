import pandas as pd


# ===== Function: 0-1 normalization
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)

    
def signal(*args):
    # Mac_v3 indicator (MAC using rolling max/min midpoint)
    # Formula: PRICE = (MAX(HIGH,N) + MIN(LOW,N))/2
    #          MAC = 10 * (MA(PRICE,N) - MA(PRICE,2N)); result = scale_01(MAC,N)
    # MAC computed on the rolling high-low midpoint, capturing the channel center rather than the candle midpoint.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    high = df['high'].rolling(n, min_periods=1).max()
    low = df['low'].rolling(n, min_periods=1).min()

    ma_short = (0.5 * high + 0.5 * low).rolling(n, min_periods=1).mean()
    ma_long = (0.5 * high + 0.5 * low).rolling(2 * n, min_periods=1).mean()

    _mac = 10 * (ma_short - ma_long)
    df[factor_name] = scale_01(_mac, n)

    return df
