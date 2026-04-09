eps = 1e-8


def signal(*args):
    # Bolling_v3 indicator (Rate of change of the Bollinger upper band)
    # Formula: UPPER = MA(CLOSE,N) + 0.5*STD(CLOSE,N)
    #          result = (UPPER - REF(UPPER, 1)) / MA
    # Measures how fast the Bollinger upper band is moving relative to the MA.
    # Positive values indicate the upper band is expanding (rising volatility); negative values indicate contraction.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['median'] = df['close'].rolling(n, min_periods=1).mean()
    df['std'] = df['close'].rolling(n).std(ddof=0)
    df['upper'] = df['median'] + 0.5 * df['std']
    df[factor_name] = (df['upper'] - df['upper'].shift(1)) / (df['median'] + eps)

    # delete extra columns
    del df['median'], df['std'], df['upper']

    return df
