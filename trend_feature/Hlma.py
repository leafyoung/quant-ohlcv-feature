def signal(*args):
    # HLMA indicator
    """
    N1=20
    N2=20
    HMA=MA(HIGH,N1)
    LMA=MA(LOW,N2)
    The HLMA indicator replaces the close price in the ordinary moving average with the high and low prices
    to get HMA and LMA respectively. A buy/sell signal is generated when the close price crosses above HMA / crosses below LMA.
    """
    df = args[0]
    n = args[1]
    factor_name = args[2]

    hma = df['high'].rolling(n, min_periods=1).mean()
    lma = df['low'].rolling(n, min_periods=1).mean()
    df['HLMA'] = hma - lma
    df['HLMA_mean'] = df['HLMA'].rolling(n, min_periods=1).mean()

    # normalize (remove units)
    df[factor_name] = df['HLMA'] / df['HLMA_mean'] - 1

    del df['HLMA']
    del df['HLMA_mean']

    return df
