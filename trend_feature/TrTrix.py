def signal(*args):
    # TrTrix indicator (single EMA percentage change)
    # Formula: EMA1 = EMA(CLOSE,N); result = EMA1.pct_change()
    # Simplified variant of TRIX using only a single EMA layer.
    # Measures the 1-period rate of change of the EMA, capturing short-term trend momentum.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['tr_trix'] = df['close'].ewm(span=n, adjust=False).mean()
    df[factor_name] = df['tr_trix'].pct_change()

    # remove redundant columns
    del df['tr_trix']

    return df
