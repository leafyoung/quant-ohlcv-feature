import pandas as pd


def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # Br indicator (Bull-Bear Ratio)
    # Formula: BR = 100 * SUM(HIGH - REF(CLOSE,1), N) / SUM(REF(CLOSE,1) - LOW, N)
    # Similar to AR but uses the previous close as the reference instead of today's open.
    # Measures willingness to push price above yesterday's close vs. below it.
    # BR > 100 suggests bullish sentiment; BR < 100 suggests bearish sentiment.
    v1 = (df['high'] - df['close'].shift(1)).rolling(n, min_periods=1).sum()
    v2 = (df['close'].shift(1) - df['low']).rolling(n, min_periods=1).sum()
    _br = 100 * v1 / v2
    df[factor_name] = pd.Series(_br)

    return df
