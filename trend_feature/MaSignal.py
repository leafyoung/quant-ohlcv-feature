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
    # MaSignal indicator (Close - MA, 0-1 normalized)
    # Formula: result = scale_01(CLOSE - MA(CLOSE, N), N)
    # Measures the deviation of close from its MA, normalized to [0,1].
    # Values above 0.5 indicate close is above the MA; below 0.5 indicates below the MA.
    s = df['close'] - df['close'].rolling(n, min_periods=1).mean()
    df[factor_name] = scale_01(s, n)

    return df
