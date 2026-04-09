import pandas as pd


# ===== Function: 0-1 normalization
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)

def signal(*args):
    # Bias36 indicator (Bias36 minus its rolling MA, 0-1 normalized)
    # Formula: BIAS36 = MA(CLOSE,3) - MA(CLOSE,6); BIAS36_MA = MA(BIAS36, N)
    #          result = scale_01(BIAS36 - BIAS36_MA, N)
    # Measures whether the short/medium MA spread (Bias36) is above or below its own average.
    # Normalized to [0,1] for comparability. High values indicate widening upward spread.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    bias36 = df['close'].rolling(3, min_periods=1).mean() - df['close'].rolling(6, min_periods=1).mean()
    bias36_ma = bias36.rolling(n, min_periods=1).mean()

    s = bias36 - bias36_ma
    df[factor_name] = scale_01(s, n)

    return df
