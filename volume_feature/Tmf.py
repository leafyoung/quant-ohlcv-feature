def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]
    # TMF indicator
    """
    N=80
    HIGH_TRUE=MAX(HIGH,REF(CLOSE,1))
    LOW_TRUE=MIN(LOW,REF(CLOSE,1))
    TMF=EMA(VOL*(2*CLOSE-HIGH_TRUE-LOW_TRUE)/(HIGH_TRUE-LOW_TRUE),N)/EMA(VOL,N)
    TMF is similar to CMF, both weighting volume by price. However, CMF uses CLV as the weight,
    while TMF uses the true low and true high prices, and takes a moving average rather than a sum.
    A buy signal is generated when TMF crosses above 0;
    a sell signal is generated when TMF crosses below 0.
    """
    df['ref'] = df['close'].shift(1)
    df['max_high'] = df[['high', 'ref']].max(axis=1)
    df['min_low'] = df[['low', 'ref']].min(axis=1)

    T = df['volume'] * ( 2 * df['close'] - df['max_high'] - df['min_low']) / (df['max_high'] - df['min_low'])
    df[factor_name] = T.ewm(n, adjust=False).mean() / df['volume'].ewm(n, adjust=False).mean()
    
    del df['ref']
    del df['max_high']
    del df['min_low']

    return df
