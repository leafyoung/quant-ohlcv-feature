def signal(*args):
    # QuoteVolumeRatio indicator
    # Formula: result = QUOTE_VOLUME / MA(QUOTE_VOLUME, N)
    # Measures the current quote volume relative to its rolling mean over N periods.
    # Values > 1 indicate above-average trading activity; values < 1 indicate below-average activity.
    df = args[0]
    n = args[1]
    factor_name = args[2]
    
    df[factor_name] = df['quote_volume'] / df['quote_volume'].rolling(n, min_periods=1).mean()

    return df
