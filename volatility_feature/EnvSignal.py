def signal(*args):
    # EnvSignal indicator (Price position relative to Envelope bands)
    # Formula: LOWER = MA(CLOSE,N) * (1 - 0.05); UPPER = MA(CLOSE,N) * (1 + 0.05)
    #          result = (CLOSE - LOWER) / (UPPER - LOWER)
    # Measures where the current close sits within the ±5% Envelope channel around the MA.
    # 0 = at the lower band; 1 = at the upper band; 0.5 = at the midline.
    # Values outside [0,1] indicate price is beyond the envelope bands.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    lower = (1 - 0.05) * df['close'].rolling(n, min_periods=1).mean()

    df[factor_name] = (df['close'] - lower) / (0.1 * df['close'].rolling(n, min_periods=1).mean())

    return df
