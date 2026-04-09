def signal(*args):
    # taker buy ratio over the past N periods
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = df['taker_buy_quote_asset_volume'].rolling(n, min_periods=1).sum() / df['quote_volume'].rolling(n, min_periods=1).sum()

    return df
