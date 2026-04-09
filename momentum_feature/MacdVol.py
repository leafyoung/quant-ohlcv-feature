def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # MACDVOL indicator
    """
    N1=20
    N2=40
    N3=10
    MACDVOL=EMA(VOLUME,N1)-EMA(VOLUME,N2)
    SIGNAL=MA(MACDVOL,N3)
    MACDVOL is the volume version of MACD. Buy when MACDVOL crosses above SIGNAL;
    sell when it crosses below SIGNAL.
    """
    N1 = 2 * n
    N2 = 4 * n
    N3 = n
    df['ema_volume_1'] = df['volume'].ewm(N1, adjust=False).mean()
    df['ema_volume_2'] = df['volume'].ewm(N2, adjust=False).mean()
    df['MACDV'] = df['ema_volume_1'] - df['ema_volume_2']
    df['SIGNAL'] = df['MACDV'].rolling(N3, min_periods=1).mean()
    # normalize
    df[factor_name] = df['MACDV'] / df['SIGNAL'] - 1
    
    del df['ema_volume_1']
    del df['ema_volume_2']
    del df['MACDV']
    del df['SIGNAL']

    return df
