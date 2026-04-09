import numpy as np


eps = 1e-8


def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # Rsimean indicator (Rolling mean of RSI)
    # Formula: RSI = A/(A+B) where A=SUM(up_diff,N), B=SUM(down_diff,N); result = MA(RSI, N)
    # Smooths RSI with a rolling mean to reduce whipsaws. Useful as a trend-following version of RSI.
    # Values above 0.5 indicate sustained buying pressure; below 0.5 indicate selling pressure.
    close_dif = df['close'].diff()
    df['up'] = np.where(close_dif > 0, close_dif, 0)
    df['down'] = np.where(close_dif < 0, abs(close_dif), 0)
    a = df['up'].rolling(n).sum()
    b = df['down'].rolling(n).sum()
    df['rsi'] = a / (a + b + eps)
    df[factor_name] = df['rsi'].rolling(n, min_periods=1).mean()

    # remove redundant columns
    del df['up'], df['down'], df['rsi']

    return df
