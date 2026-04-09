def signal(*args):
    # AvgPriceToHigh indicator (VWAP relative to current High)
    # Formula: VWAP = SUM(QUOTE_VOLUME,N) / SUM(VOLUME,N); result = VWAP / HIGH - 1
    # Measures whether the N-period VWAP is above or below the current candle's high.
    # Negative values (typical) indicate VWAP is below the high; values near 0 suggest price is near VWAP.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['price'] = df['quote_volume'].rolling(n, min_periods=1).sum() / df['volume'].rolling(n, min_periods=1).sum()
    df[factor_name] = df['price'] / df['high'] - 1

    # remove redundant columns
    del df['price']

    return df
