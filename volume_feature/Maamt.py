def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # MAAMT indicator
    """
    N=40
    MAAMT=MA(AMOUNT,N)
    MAAMT is a moving average of trading volume. Buy/sell signals are generated
    when volume crosses above/below the moving average.
    """
    MAAMT = df['volume'].rolling(n, min_periods=1).mean()
    df[factor_name] = (df['volume'] - MAAMT) / MAAMT  # avoid dimensionality issues

    return df
