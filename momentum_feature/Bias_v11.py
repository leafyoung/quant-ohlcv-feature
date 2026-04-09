def signal(*args):
    # Bias_v11 indicator (Volume-weighted Bias with EMA smoothing)
    # Formula: BIAS = CLOSE/MA(CLOSE,N) - 1; VOL_RATIO = QUOTE_VOLUME / MA(QUOTE_VOLUME,N)
    #          MTM = BIAS * VOL_RATIO; result = EMA(MTM, N)
    # Volume-weighted price bias: amplifies signal when above-average volume accompanies the price deviation.
    # EMA smoothing reduces noise. High positive values indicate volume-backed upside momentum.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['ma'] = df['close'].rolling(n, min_periods=1).mean()
    df['mtm'] = (df['close'] / df['ma'] - 1) * df['quote_volume'] / df['quote_volume'].rolling(n, min_periods=1).mean()
    # EMA
    df[factor_name] = df['mtm'].ewm(n, adjust=False).mean()

    del df['ma'], df['mtm']

    return df
