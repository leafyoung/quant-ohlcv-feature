def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # LMA indicator
    """
    N=20
    LMA=MA(LOW,N)
    LMA is a simple moving average with the closing price replaced by the lowest price.
    Buy/sell signals are generated when the low crosses above/below LMA.
    """
    df['low_ma'] = df['low'].rolling(n, min_periods=1).mean()
    # normalize
    df[factor_name] = df['low'] / df['low_ma'] - 1

    del df['low_ma']

    return df
