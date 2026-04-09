def signal(*args):
    # TakerByRatioPerTrade indicator
    # Formula: TAKER_RATIO = SUM(taker_buy_quote,N) / SUM(quote_volume,N)
    #          result = TAKER_RATIO / MA(trade_num, N)
    # Normalizes the taker buy ratio by average number of trades per period.
    # Captures buy-side dominance per unit of market activity — useful for detecting
    # large directional orders relative to typical trade frequency.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    volume = df['quote_volume'].rolling(n, min_periods=1).sum()
    buy_volume = df['taker_buy_quote_asset_volume'].rolling(n, min_periods=1).sum()

    df["trade_mean"] = df['trade_num'].rolling(n, min_periods=1).mean()
    df[factor_name] = buy_volume / volume / df["trade_mean"]

    return df
