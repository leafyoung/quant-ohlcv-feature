import numpy as np


def signal(*args):
    # DO indicator
    """
    DO=EMA(EMA(RSI,N),M)
    DO is the RSI indicator after smoothing (double moving average). DO greater than 0 indicates
    the market is in an uptrend, less than 0 indicates a downtrend. We use DO crossing above/below
    its moving average to generate buy/sell signals.
    """
    df = args[0]
    n = args[1]
    factor_name = args[2]

    diff = df['close'].diff()
    df['up'] = np.where(diff > 0, diff, 0)
    df['down'] = np.where(diff < 0, abs(diff), 0)
    A = df['up'].rolling(n).sum()
    B = df['down'].rolling(n).sum()
    df['rsi'] = A / (A + B)
    df['ema_rsi'] = df['rsi'].ewm(n, adjust=False).mean()
    df[factor_name] = df['ema_rsi'].ewm(n, adjust=False).mean()

    del df['up']
    del df['down']
    del df['rsi']
    del df['ema_rsi']

    return df
