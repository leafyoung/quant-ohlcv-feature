import pandas as pd


# ===== Function: 0-1 normalization
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)


def signal(*args):
    # Mac indicator (MA Convergence: short-long MA difference, 0-1 normalized)
    # Formula: MAC = 10 * (MA(CLOSE,N) - MA(CLOSE,2N)); result = scale_01(MAC, N)
    # Measures the difference between short and long moving averages (similar to MACD without EMA).
    # Positive values indicate short MA above long MA (uptrend); negative indicates downtrend.
    # MAC

    df = args[0]
    n = args[1]
    factor_name = args[2]

    ma_short = df['close'].rolling(n, min_periods=1).mean()
    ma_long = df['close'].rolling(2 * n, min_periods=1).mean()

    _mac = 10 * (ma_short - ma_long)
    df[factor_name] = scale_01(_mac, n)

    return df
