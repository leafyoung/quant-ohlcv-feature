def signal(*args):
    # Mtm multiplied by volatility, where volatility is expressed as the ratio of high to low
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['mtm'] = df['close'] / df['close'].shift(n) - 1
    df['volatility'] = df['high'].rolling(n, min_periods=1).max() / df['low'].rolling(n, min_periods=1).min() - 1
    df[factor_name] = df['mtm'].rolling(window=n, min_periods=1).mean() * df['volatility']

    del df['mtm'], df['volatility']

    return df
