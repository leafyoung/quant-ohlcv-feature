def signal(*args):
    # MtmMean indicator (Rolling mean of N-period momentum)
    # Formula: MTM = CLOSE/REF(CLOSE,N)-1; result = MA(MTM, N)
    # Smooths the N-period momentum by taking its rolling mean, reducing noise.
    # Positive values indicate sustained upward price trend; negative indicates downward trend.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = (df['close'] / df['close'].shift(n) - 1).rolling(window=n, min_periods=1).mean()

    return df
