def signal(*args):
    # How many minutes in the past n minutes showed a price increase
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['_ret_sign'] = df['close'].pct_change() > 0
    df[factor_name] = df['_ret_sign'].rolling(n, min_periods=1).sum()

    del df['_ret_sign']

    return df
