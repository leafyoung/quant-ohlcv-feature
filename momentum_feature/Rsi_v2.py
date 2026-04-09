import numpy as np


eps = 1e-8


def signal(*args):
    # Rsi_v2 indicator (RSI using rolling sum instead of EWM)
    # Formula: A = SUM(MAX(DIFF,0), N); B = SUM(MAX(-DIFF,0), N)
    #          result = A / (A + B)
    # Standard RSI computed using rolling sum (Wilder-style but without EWM).
    # Range [0, 1]. Values above 0.7 indicate overbought; below 0.3 indicate oversold.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    close_dif = df['close'].diff()
    df['up'] = np.where(close_dif > 0, close_dif, 0)
    df['down'] = np.where(close_dif < 0, abs(close_dif), 0)
    a = df['up'].rolling(n).sum()
    b = df['down'].rolling(n).sum()
    df[factor_name] = a / (a + b + eps)

    # remove redundant columns
    del df['up'], df['down']

    return df
