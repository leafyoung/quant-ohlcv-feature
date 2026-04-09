def signal(*args):
    # SrocVol indicator (SROC applied to volume)
    # Formula: EMAP = EMA(VOLUME, 2N); result = (EMAP - REF(EMAP, N)) / REF(EMAP, N)
    # Measures the N-period rate of change of the long EMA of volume.
    # Positive values indicate volume trend is accelerating upward; negative indicates it's declining.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # EMAP=EMA(VOLUME,N)
    df['emap'] = df['volume'].ewm(2 * n, adjust=False).mean()
    # SROCVOL=(EMAP-REF(EMAP,M))/REF(EMAP,M)
    df[factor_name] = (df['emap'] - df['emap'].shift(n)) / df['emap'].shift(n)

    del df['emap']

    return df
