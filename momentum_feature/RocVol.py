def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]
    # RocVol indicator
    """
    N = 80
    RocVol=(VOLUME-REF(VOLUME,N))/REF(VOLUME,N)
    RocVol is the volume version of ROC. Buy when RocVol crosses above 0;
    sell when it crosses below 0.
    """
    df[factor_name] = df['volume'] / df['volume'].shift(n) - 1

    return df
