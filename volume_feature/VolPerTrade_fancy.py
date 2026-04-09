def signal(*args):
    # Average trade size per transaction, checking if large orders appeared in this minute
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = df['quote_volume'].rolling(n, min_periods=1).sum() / df['trade_num'].rolling(n, min_periods=1).sum()

    return df
