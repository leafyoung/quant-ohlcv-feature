import numpy as np
import pandas as pd


# ===== function: 0-1 normalization
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)


def signal(*args):
    # DzrsiUpperSignal indicator (RSI half-period MA - RSI Bollinger Upper band, 0-1 normalized)
    # Formula: RSI = A / (A + B) where A=SUM(up_diff,N), B=SUM(down_diff,N)
    #          RSI_UPPER = MA(RSI,N) + 2*STD(RSI,N); RSI_MA = MA(RSI, N/2)
    #          result = scale_01(RSI_MA - RSI_UPPER, N)
    # Measures how far the RSI half-period MA is below the RSI upper Bollinger band.
    # Low values indicate RSI is at or above the upper band (overbought conditions).
    df = args[0]
    n = args[1]
    factor_name = args[2]

    rtn = df['close'].diff()
    up = np.where(rtn > 0, rtn, 0)
    dn = np.where(rtn < 0, rtn.abs(), 0)
    a = pd.Series(up).rolling(n, min_periods=1).sum()
    b = pd.Series(dn).rolling(n, min_periods=1).sum()

    a *= 1e3
    b *= 1e3

    rsi = a / (1e-9 + a + b)

    rsi_middle = rsi.rolling(n, min_periods=1).mean()
    rsi_upper = rsi_middle + 2 * rsi.rolling(n, min_periods=1).std()
    # rsi_lower = rsi_middle - 2 * rsi.rolling(n, min_periods=1).std()
    rsi_ma = rsi.rolling(int(n / 2), min_periods=1).mean()

    s = rsi_ma - rsi_upper
    df[factor_name] = scale_01(s, n)

    return df
