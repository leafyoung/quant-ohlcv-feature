import numpy as np


def signal(*args):
    # Grid indicator (z-score grid position percentage change)
    # Formula: MA = MA(CLOSE,N); STD = STD(CLOSE,N)
    #          GRID = MA((CLOSE - MA) / STD, N)  (rolling mean of z-scores)
    #          result = GRID.pct_change(N)
    # Measures the N-period rate of change of the smoothed z-score position.
    # Captures acceleration of price relative to its own volatility band.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['median'] = df['close'].rolling(n, min_periods=1).mean()
    df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)
    df['grid'] = (df['close'] - df['median']) / df['std']
    df['grid'] = df['grid'].replace([np.inf, -np.inf], np.nan)
    df['grid'].fillna(value=0, inplace=True)
    df['grid'] = df['grid'].rolling(window=n).mean()
    df[factor_name] = df['grid'].pct_change(n)
    # df['gridInt'] = df['grid'].astype("int")
    # df[factor_name] = df['gridInt'].pct_change(n)

    del df['median'], df['std'], df['grid']  # , df['gridInt']

    return df
