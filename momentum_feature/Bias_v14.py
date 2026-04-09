def signal(*args):
    # Bias_v14 indicator (Volume-weighted fast/slow MA bias, rolling mean)
    # Formula: MA = MA(CLOSE,N); MAFAST = MA(CLOSE,N/2)
    #          MTM = (MAFAST/MA - 1) * (QUOTE_VOLUME / MA(QUOTE_VOLUME,N))
    #          result = MA(MTM, N)
    # Volume-weighted version of the fast/slow MA bias (Bias_v13), amplified by relative quote volume.
    # Positive rolling mean indicates sustained volume-backed uptrend.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['ma'] = df['close'].rolling(n, min_periods=1).mean()
    df['ma2'] = df['close'].rolling(int(n/2), min_periods=1).mean()
    df['mtm'] = (df['ma2'] / df['ma'] - 1) * df['quote_volume']/df['quote_volume'].rolling(n, min_periods=1).mean()
    df[factor_name] = df['mtm'].rolling(n, min_periods=1).mean()

    del df['ma'],df['ma2'],df['mtm']

    return df
