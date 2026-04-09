import numpy as np
import pandas as pd


eps = 1e-8


def signal(*args):
    # Rsis indicator (RSI normalized to its rolling min/max range)
    # Formula: RSI = 100 * EMA(up_diff, 4N) / EMA(|diff|, 4N) (smoothed via EWM)
    #          RSIS = 100 * (RSI - MIN(RSI, 4N)) / (MAX(RSI, 4N) - MIN(RSI, 4N))
    # Normalizes RSI to its historical [0, 100] range over 4N periods, improving cross-asset comparability.
    # Values near 100 indicate RSI is near its highest recent level; near 0 near its lowest.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    close_diff_pos = np.where(df['close'] > df['close'].shift(
        1), df['close'] - df['close'].shift(1), 0)
    rsi_a = pd.Series(close_diff_pos).ewm(
        alpha=1 / (4 * n), adjust=False).mean()
    rsi_b = (df['close'] - df['close'].shift(1)
             ).abs().ewm(alpha=1 / (4 * n), adjust=False).mean()
    rsi = 100 * rsi_a / (eps + rsi_b)
    rsi_min = pd.Series(rsi).rolling(int(4 * n), min_periods=1).min()
    rsi_max = pd.Series(rsi).rolling(int(4 * n), min_periods=1).max()
    rsis = 100 * (rsi - rsi_min) / (eps + rsi_max - rsi_min)
    df[factor_name] = pd.Series(rsis)    

    return df
