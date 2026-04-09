def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # AMV indicator
    """
    N1=13
    N2=34
    AMOV=VOLUME*(OPEN+CLOSE)/2
    AMV1=SUM(AMOV,N1)/SUM(VOLUME,N1)
    AMV2=SUM(AMOV,N2)/SUM(VOLUME,N2)
    AMV uses trading volume as a weight for the volume-weighted moving average of the
    average of open and close prices. Higher-volume prices have a greater impact on the
    moving average result, reducing the influence of low-volume price fluctuations.
    A buy/sell signal is generated when the short-term AMV line crosses above/below the long-term AMV line.
    """
    df['AMOV'] = df['volume'] * (df['open'] + df['close']) / 2
    df['AMV1'] = df['AMOV'].rolling(n).sum() / df['volume'].rolling(n).sum()
    # df['AMV2'] = df['AMOV'].rolling(n * 3).sum() / df['volume'].rolling(n * 3).sum()
    # normalize
    df[factor_name] = (df['AMV1'] - df['AMV1'].rolling(n).min()) / (df['AMV1'].rolling(n).max() - df['AMV1'].rolling(n).min()) # normalize
    
    del df['AMOV']
    del df['AMV1']

    return df
