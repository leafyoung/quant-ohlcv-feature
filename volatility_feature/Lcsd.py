eps = 1e-8


def signal(*args):
    # Lcsd indicator (Low price vs Close MA ratio)
    # Formula: result = (LOW - MA(CLOSE, N)) / LOW
    # Measures how far the low price is below the rolling close MA, as a fraction of the low.
    # Negative values indicate the MA is above the low (price recently been higher than current low).
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['median'] = df['close'].rolling(n).mean()
    df[factor_name] = (df['low'] - df['median']) / (df['low'] + eps)

    # remove redundant columns
    del df['median']

    return df
