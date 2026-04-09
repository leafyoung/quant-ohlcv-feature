def signal(*args):
    # Bias indicator (Price deviation from MA)
    # Formula: BIAS = CLOSE / MA(CLOSE, N) - 1
    # Measures how far the close price deviates from its N-period moving average as a percentage.
    # Positive values indicate price is above MA (overbought potential); negative values indicate below MA (oversold potential).
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['ma'] = df['close'].rolling(n, min_periods=1).mean()
    df[factor_name] = (df['close'] / df['ma'] - 1)

    del df['ma']

    return df
