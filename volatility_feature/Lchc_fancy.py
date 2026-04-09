def signal(*args):
    # Ratio of current price to the highest and lowest prices over the past N minutes, checking whether upward or downward momentum is stronger
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = -1 * df['low'].rolling(n, min_periods=1).min() / df['close'] - df['high'].rolling(n, min_periods=1).max() / df['close']

    return df
