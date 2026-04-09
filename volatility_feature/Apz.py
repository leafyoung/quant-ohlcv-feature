def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    """
    N=10
    M=20
    PARAM=2
    VOL=EMA(EMA(HIGH-LOW,N),N)
    UPPER=EMA(EMA(CLOSE,M),M)+PARAM*VOL
    LOWER= EMA(EMA(CLOSE,M),M)-PARAM*VOL
    APZ (Adaptive Price Zone) is similar to Bollinger Bands and the Keltner Channel:
    all are price channels built around a moving average based on price volatility.
    The difference lies in how volatility is measured: Bollinger Bands use the standard
    deviation of the close, the Keltner Channel uses the true range ATR, and APZ uses
    the N-day double exponential average of the high-low difference to measure price amplitude.
    """
    df['hl'] = df['high'] - df['low']
    df['ema_hl'] = df['hl'].ewm(n, adjust=False).mean()
    df['vol'] = df['ema_hl'].ewm(n, adjust=False).mean()

    # calculate the channel; can be used as a CTA strategy or adapted as a factor
    df['ema_close'] = df['close'].ewm(2 * n, adjust=False).mean()
    df['ema_ema_close'] = df['ema_close'].ewm(2 * n, adjust=False).mean()
    # normalize using EMA
    df[factor_name] = df['vol'] / df['ema_ema_close']

    del df['hl']
    del df['ema_hl']
    del df['vol']
    del df['ema_close']
    del df['ema_ema_close']

    return df
