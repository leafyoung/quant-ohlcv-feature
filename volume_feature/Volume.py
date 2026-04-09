def signal(*args):
    # Volume indicator (Rolling sum of quote volume)
    # Formula: result = SUM(QUOTE_VOLUME, N)
    # Sums quote volume over N periods, representing the total traded dollar value in the window.
    # A simple measure of market participation and liquidity over recent candles.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = df['quote_volume'].rolling(n, min_periods=1).sum()

    return df
