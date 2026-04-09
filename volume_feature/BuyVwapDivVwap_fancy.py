def signal(*args):
    # ratio of taker buy VWAP to current VWAP.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['vwap'] = df['quote_volume'].rolling(n, min_periods=1).sum() / df['volume'].rolling(n, min_periods=1).sum()
    df['buy_vwap'] = df['taker_buy_quote_asset_volume'].rolling(n, min_periods=1).sum() / df['taker_buy_base_asset_volume'].rolling(n, min_periods=1).sum()
    df[factor_name] = df['buy_vwap'] / df['vwap']

    del df['vwap'], df['buy_vwap']

    return df
