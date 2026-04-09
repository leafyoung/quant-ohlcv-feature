import numpy as np
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
    # ******************** TDI ********************
    # RSI_PriceLine=EMA(RSI,N2)
    # RSI_SignalLine=EMA(RSI,N3)
    # RSI_MarketLine=EMA(RSI,N4)
    # TDI is a technical indicator derived from RSI, including RSI price line, trade signal line, market baseline, etc.
    # Buy/sell signals are generated when the RSI price line simultaneously crosses above/below the trade signal line and market baseline.

    rtn = df['close'].diff()
    up = np.where(rtn > 0, rtn, 0)
    dn = np.where(rtn < 0, rtn.abs(), 0)
    a = pd.Series(up).rolling(n, min_periods=1).sum()
    b = pd.Series(dn).rolling(n, min_periods=1).sum()
    a *= 1e3
    b *= 1e3
    rsi = a / (1e-9 + a + b)
    rsi_price_line = pd.Series(rsi).ewm(span=n, adjust=False, min_periods=1).mean()
    rsi_signal_line = pd.Series(rsi).ewm(span=int(2 * n), adjust=False, min_periods=1).mean()

    s = rsi_price_line - rsi_signal_line
    df[factor_name] = scale_01(s, n)

    return df
