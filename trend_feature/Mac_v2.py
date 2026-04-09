import pandas as pd


# ===== Function: 0-1 normalization
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)

    
def signal(*args):
    # Mac_v2 indicator (MAC using (H+L)/2 price)
    # Formula: PRICE = (HIGH+LOW)/2; MAC = 10 * (MA(PRICE,N) - MA(PRICE,2N)); result = scale_01(MAC,N)
    # MA convergence computed on the midpoint price instead of close.
    # More representative of the full candle range than close-only MAC.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    ma_short = (0.5 * df['high'] + 0.5 * df['low']).rolling(n, min_periods=1).mean()
    ma_long = (0.5 * df['high'] + 0.5 * df['low']).rolling(2 * n, min_periods=1).mean()

    _mac = 10 * (ma_short - ma_long)
    df[factor_name] = scale_01(_mac, n)

    return df
