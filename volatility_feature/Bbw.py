import numpy as np


eps = 1e-8


def signal(*args):
    # Bbw indicator (BBW change × momentum × RSI composite)
    # Formula: RSI = 100 * A/(A+B) where A=SUM(up_diff,N), B=SUM(down_diff,N)
    #          BBW = STD(CLOSE,N)/MA(CLOSE,N); BBW_CHG = BBW.diff(N)
    #          result = BBW_CHG * (CLOSE/REF(CLOSE,N) - 1) * RSI
    # Combines Bollinger bandwidth change (volatility expansion/contraction) with N-period
    # momentum and RSI. Positive values indicate expanding volatility with upside momentum.
    df = args[0]
    n = args[1]
    factor_name = args[2]
    
    close_dif = df['close'].diff()
    df['up'] = np.where(close_dif > 0, close_dif, 0)
    df['down'] = np.where(close_dif < 0, abs(close_dif), 0)
    a = df['up'].rolling(n).sum()
    b = df['down'].rolling(n).sum()
    df['rsi'] = (a / (a + b)) * 100
    df['median'] = df['close'].rolling(n, min_periods=1).mean()
    df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)
    df['bbw'] = (df['std'] / df['median']).diff(n)
    df[factor_name] = (df['bbw']) * (df['close'] / df['close'].shift(n) - 1 + eps) * df['rsi']

    del df['up'], df['down'],  df['rsi'], df['median']
    del df['std'], df['bbw']

    return df
