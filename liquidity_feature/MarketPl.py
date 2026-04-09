eps = 1e-8


def signal(*args):
    # MarketPl indicator
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # MarketPl indicator (Market Placement / Average Holding Cost)
    # Formula: AVG_COST = EMA(QUOTE_VOLUME, N) / EMA(VOLUME, N); result = CLOSE / AVG_COST - 1
    # Computes EMA-weighted average holding cost (VWAP-like using EMA smoothing),
    # then measures how far the current close is above or below this cost.
    # Positive values suggest the current price is above average holding cost (profitable for holders).
    quote_volume_ema = df['quote_volume'].ewm(span=n, adjust=False).mean()
    volume_ema = df['volume'].ewm(span=n, adjust=False).mean()
    df['avg_holding_cost'] = quote_volume_ema / volume_ema
    df[factor_name] = df['close'] / (df['avg_holding_cost'] + eps) - 1

    del df['avg_holding_cost']

    return df
