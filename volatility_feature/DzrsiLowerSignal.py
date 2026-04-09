import numpy as np
import pandas as pd


# ===== function: zscore normalization
def scale_zscore(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).mean()
          ) / pd.Series(_s).rolling(_n, min_periods=1).std()
    return pd.Series(_s)


def signal(*args):
    # DzrsiLowerSignal indicator (RSI Bollinger Lower band - RSI half-period MA, z-score normalized)
    # Formula: RSI = A / (A + B) where A=SUM(up_diff,N), B=SUM(down_diff,N)
    #          RSI_LOWER = MA(RSI,N) - 2*STD(RSI,N); RSI_MA = MA(RSI, N/2)
    #          result = ZSCORE(RSI_LOWER - RSI_MA, N)
    # Applies Bollinger Band logic to RSI. Measures how far the RSI lower band is below the
    # RSI half-period MA, z-score normalized. Negative values suggest RSI is below its lower band (oversold).
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
    # rsi_upper = rsi_middle + 2 * rsi.rolling(n, min_periods=1).std()
    rsi_lower = rsi_middle - 2 * rsi.rolling(n, min_periods=1).std()
    rsi_ma = rsi.rolling(int(n / 2), min_periods=1).mean()

    s = rsi_lower - rsi_ma
    df[factor_name] = scale_zscore(s, n)

    return df
