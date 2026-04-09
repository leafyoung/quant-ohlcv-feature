eps = 1e-8


def signal(*args):
    # Tma indicator (Close vs double Moving Average)
    # Formula: MA1 = MA(CLOSE,N); MA2 = MA(MA1,N); result = CLOSE / (MA2 + eps) - 1
    # Uses a double-smoothed MA (Triangular MA) as the trend baseline.
    # Positive values indicate close is above the double MA (upward bias); negative below.
    df = args[0]
    n = args[1]
    factor_name = args[2]
    
    df['ma'] = df['close'].rolling(n, min_periods=1).mean()
    df['ma2'] = df['ma'].rolling(n, min_periods=1).mean()
    df[factor_name] = df['close'] / (df['ma2'] + eps) - 1

    # remove redundant columns
    del df['ma'], df['ma2']

    return df
