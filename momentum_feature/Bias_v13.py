def signal(*args):
    # Bias_v13 indicator (Fast MA / Slow MA bias, rolling mean)
    # Formula: MAFAST = MA(CLOSE, N/2); MASLOW = MA(CLOSE, N)
    #          result = MA(MAFAST/MASLOW - 1, N)
    # Measures the smoothed ratio of a short-window MA to a long-window MA.
    # Positive values indicate short MA is consistently above long MA (uptrend); negative indicates downtrend.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['ma'] = df['close'].rolling(n, min_periods=1).mean()
    df['mafast'] = df['close'].rolling(int(n/2), min_periods=1).mean()
    df[factor_name] = (df['mafast'] / df['ma'] - 1).rolling(n, min_periods=1).mean()

    del df['ma'],df['mafast']

    return df
