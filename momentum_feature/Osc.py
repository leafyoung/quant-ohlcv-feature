def signal(*args):

    # OSC indicator
    """
    N=40
    M=20
    OSC=CLOSE-MA(CLOSE,N)
    OSCMA=MA(OSC,M)
    OSC reflects the degree to which the closing price deviates from its moving average.
    Buy/sell signals are generated when OSC crosses above/below OSCMA.
    """
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['ma'] = df['close'].rolling(2 * n, min_periods=1).mean()
    df['OSC'] = df['close'] - df['ma']
    df[factor_name] = df['OSC'].rolling(n, min_periods=1).mean()

    del df['ma']
    del df['OSC']

    return df
