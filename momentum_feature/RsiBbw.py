import numpy as np


eps = 1e-8


def signal(*args):
    # RsiBbw indicator (BBW change × momentum × RSI composite)
    # Formula: RSI = 100 * A/(A+B) where A=SUM(up_diff,N), B=SUM(down_diff,N)
    #          BBW_CHG = (STD/MA).diff(N); MTM = CLOSE/REF(CLOSE,N)-1
    #          result = BBW_CHG * MTM * RSI
    # Combines Bollinger bandwidth change, N-period price momentum, and RSI level.
    # Positive values suggest expanding volatility with upside momentum and elevated RSI.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    close_dif = df['close'].diff()
    df['up'] = np.where(close_dif > 0, close_dif, 0)
    df['down'] = np.where(close_dif < 0, abs(close_dif), 0)
    a = df['up'].rolling(n).sum()
    b = df['down'].rolling(n).sum()
    df['rsi'] = (a / (a+b+eps)) * 100
    df['median'] = df['close'].rolling(n, min_periods=1).mean()
    df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)
    df['bbw'] = (df['std'] / df['median']).diff(n)
    df[factor_name] = (df['bbw']) * (df['close'] / df['close'].shift(n) - 1) * df['rsi']

    del df['up'], df['down'], df['rsi'], df['median'], df['std'], df['bbw']

    return df
