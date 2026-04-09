def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # BIASVOL indicator
    """
    N=6，12，24
    BIASVOL(N)=(VOLUME-MA(VOLUME,N))/MA(VOLUME,N)
    BIASVOL is the volume version of the BIAS (deviation rate) indicator. A buy signal is
    generated when BIASVOL6 > 5 and BIASVOL12 > 7 and BIASVOL24 > 11;
    a sell signal is generated when BIASVOL6 < -5 and BIASVOL12 < -7 and BIASVOL24 < -11.
    """
    df['ma_volume'] = df['volume'].rolling(n, min_periods=1).mean()
    df[factor_name] = (df['volume'] - df['ma_volume']) / df['ma_volume']

    del df['ma_volume']

    return df
