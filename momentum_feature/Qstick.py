def signal(*args):
    # Qstick indicator
    """
    N=20
    Qstick=MA(CLOSE-OPEN,N)
    Qstick reflects the direction and strength of price trends by comparing closing and opening prices.
    Buy/sell signals are generated when Qstick crosses above/below 0.
    """
    df = args[0]
    n = args[1]
    factor_name = args[2]

    cl = df['close'] - df['open']
    Qstick = cl.rolling(n, min_periods=1).mean()
    # normalize
    df[factor_name] = cl / Qstick - 1

    return df
