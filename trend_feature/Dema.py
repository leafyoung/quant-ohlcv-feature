eps = 1e-8


def signal(*args):
    # Dema indicator
    df = args[0]
    n = args[1]
    factor_name = args[2]

    """
    N=60
    EMA=EMA(CLOSE,N)
    DEMA=2*EMA-EMA(EMA,N)
    DEMA combines single EMA and double EMA to reduce lag while maintaining smoothness.
    """
    ema = df['close'].ewm(n, adjust=False).mean()  # EMA=EMA(CLOSE,N)
    ema_ema = ema.ewm(n, adjust=False).mean()  # EMA(EMA,N)
    dema = 2 * ema - ema_ema  # DEMA=2*EMA-EMA(EMA,N)
    # normalize dema
    df[factor_name] = dema / (ema + eps) - 1

    return df
