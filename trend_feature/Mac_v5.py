import pandas as pd


# ===== Function: 0-1 normalization
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)


def signal(*args):
    # Mac_v5 indicator (MAC using (rolling high + rolling low + open)/3)
    # Formula: PRICE = (MAX(HIGH,N) + MIN(LOW,N) + OPEN) / 3
    #          MAC = 10 * (MA(PRICE,N) - MA(PRICE,2N)); result = scale_01(MAC,N)
    # Uses a modified price that replaces close with open, alongside rolling high/low extremes.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    high = df['high'].rolling(n, min_periods=1).max()
    low = df['low'].rolling(n, min_periods=1).min()
    _open = df['open']

    ma_short = ((high + low + _open) / 3.).rolling(n, min_periods=1).mean()
    ma_long = ((high + low + _open) / 3.).rolling(2 * n, min_periods=1).mean()

    _mac = 10 * (ma_short - ma_long)
    df[factor_name] = scale_01(_mac, n)

    return df
