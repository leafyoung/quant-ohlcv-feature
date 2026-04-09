def signal(*args):
    # Bolling_fancy indicator (Z-score position relative to Bollinger bands)
    # Formula: result = (CLOSE - MA(CLOSE,N)) / STD(CLOSE,N)
    # Standard z-score of close price within its rolling distribution over N periods.
    # Equivalent to the Bollinger %b scaled to z-score units. Positive = above mean; negative = below.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = (df['close'] - df['close'].rolling(n, min_periods=1).mean()) / df['close'].rolling(n, min_periods=1).std()

    return df
