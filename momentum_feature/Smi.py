def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]
    # SMI indicator
    """
    N1=20
    N2=20
    N3=20
    M=(MAX(HIGH,N1)+MIN(LOW,N1))/2
    D=CLOSE-M
    DS=EMA(EMA(D,N2),N2)
    DHL=EMA(EMA(MAX(HIGH,N1)-MIN(LOW,N1),N2),N2)
    SMI=100*DS/DHL
    SMIMA=MA(SMI,N3)
    SMI can be seen as a variant of KDJ. The difference is that KD measures where today's
    closing price falls between the highest and lowest prices over the past N days, while SMI
    measures the distance between today's closing price and the midpoint of those extremes.
    Buy/sell signals are generated when SMI crosses above/below its moving average.
    """
    df['max_high'] = df['high'].rolling(n, min_periods=1).mean()
    df['min_low'] = df['low'].rolling(n, min_periods=1).mean()
    df['M'] = (df['max_high'] + df['min_low']) / 2
    df['D'] = df['close'] - df['M']
    df['ema'] = df['D'].ewm(n, adjust=False).mean()
    df['DS'] = df['ema'].ewm(n, adjust=False).mean()
    df['HL'] = df['max_high'] - df['min_low']
    df['ema_hl'] = df['HL'].ewm(n, adjust=False).mean()
    df['DHL'] = df['ema_hl'].ewm(n, adjust=False).mean()
    df['SMI'] = 100 * df['DS'] / df['DHL']
    df[factor_name] = df['SMI'].rolling(n, min_periods=1).mean()

    del df['max_high']
    del df['min_low']
    del df['M']
    del df['D']
    del df['ema']
    del df['DS']
    del df['HL']
    del df['ema_hl']
    del df['DHL']
    del df['SMI']

    return df
