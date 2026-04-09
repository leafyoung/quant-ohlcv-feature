def signal(*args):
    """
    The maximum of average maximum drawdown and average maximum reverse drawdown over a period forms the Market Sentiment Stability Index.
    Market Sentiment Stability Index
    The smaller the indicator, the stronger the trend.
    """
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['max2here'] = df['high'].rolling(n, min_periods=1).max()
    df['dd1here'] = abs(df['close']/df['max2here'] - 1)
    df['avg_max_drawdown'] = df['dd1here'].rolling(n, min_periods=1).mean()

    df['min2here'] = df['low'].rolling(n, min_periods=1).min()
    df['dd2here'] = abs(df['close'] / df['min2here'] - 1)
    df['avg_reverse_drawdown'] = df['dd2here'].rolling(n, min_periods=1).mean()

    df[factor_name] = df[['avg_max_drawdown', 'avg_reverse_drawdown']].max(axis=1)

    del df['max2here']
    del df['dd1here']
    del df['avg_max_drawdown']
    del df['min2here']
    del df['dd2here']
    del df['avg_reverse_drawdown']

    return df
