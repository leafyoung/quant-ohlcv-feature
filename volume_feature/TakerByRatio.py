def signal(*args):
    # TakerByRatio indicator
    # Formula: result = SUM(taker_buy_quote_asset_volume, N) / SUM(quote_volume, N)
    # Measures the fraction of quote volume that was initiated by buyers (taker buys) over N periods.
    # Values close to 1 indicate strong buying pressure; values close to 0 indicate selling pressure.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    volume = df['quote_volume'].rolling(n, min_periods=1).sum()
    buy_volume = df['taker_buy_quote_asset_volume'].rolling(n, min_periods=1).sum()
    df[factor_name] = buy_volume / volume

    return df

