eps = 1e-8


def signal(*args):
    # AvgPrice indicator (VWAP normalized within rolling range)
    # Formula: VWAP = SUM(QUOTE_VOLUME,N) / SUM(VOLUME,N)
    #          result = (VWAP - MIN(VWAP,N)) / (MAX(VWAP,N) - MIN(VWAP,N) + eps)
    # Computes a rolling VWAP (volume-weighted average price) and normalizes it to [0,1]
    # within its N-period range. Values near 1 indicate VWAP is near its recent high; near 0 near its low.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['price'] = df['quote_volume'].rolling(n, min_periods=1).sum() / df['volume'].rolling(n, min_periods=1).sum()
    df[factor_name] = (df['price'] - df['price'].rolling(n, min_periods=1).min()) / (
        df['price'].rolling(n, min_periods=1).max() - df['price'].rolling(n, min_periods=1).min() + eps)

    # remove redundant columns
    del df['price']

    return df
