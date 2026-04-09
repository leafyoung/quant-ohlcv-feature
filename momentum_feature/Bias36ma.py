def signal(*args):
    # Bias36ma indicator (Rolling MA of MA3-MA6 bias)
    # Formula: BIAS36 = MA(CLOSE, 3) - MA(CLOSE, 6); result = MA(BIAS36, N)
    # Measures the smoothed difference between short (3-period) and medium (6-period) moving averages.
    # Positive values indicate short MA is above long MA (uptrend); negative indicates downtrend.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    bias36 = df['close'].rolling(3, min_periods=1).mean() - df['close'].rolling(6, min_periods=1).mean()
    df[factor_name] = bias36.rolling(n, min_periods=1).mean()

    return df
