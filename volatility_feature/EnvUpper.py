import pandas as pd


# ===== Function: 0-1 normalization
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)


def signal(*args):
    # EnvUpper indicator (Envelope upper band, 0-1 normalized)
    # Formula: UPPER = MA(CLOSE, N) * (1 + 0.05); result = scale_01(UPPER, N)
    # Computes the upper band of an Envelope channel (MA ± 5%) and normalizes to [0,1].
    # Envelope channels are used to identify overbought/oversold levels relative to a percentage
    # offset from the moving average.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    upper = (1 + 0.05) * df['close'].rolling(n, min_periods=1).mean()

    s = upper
    df[factor_name] = scale_01(s, n)

    return df
