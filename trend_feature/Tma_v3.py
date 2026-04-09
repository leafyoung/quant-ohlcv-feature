def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]
    # TMA indicator
    """
    N=20
    CLOSE_MA=MA(CLOSE,N)
    TMA=MA(CLOSE_MA,N)
    TMA is similar to other moving averages, but unlike EMA which gives more weight to prices
    closer to the current day, TMA gives more weight to prices in the middle of the considered
    time window. Buy/sell signals are generated when price crosses above/below TMA.
    """
    _ts = (df["high"].rolling(n, min_periods=1).max() + df["low"].rolling(n, min_periods=1).min()) / 2.

    close_ma = _ts.rolling(n, min_periods=1).mean()
    tma = close_ma.rolling(n, min_periods=1).mean()
    df[factor_name] = df["close"] / tma - 1

    return df
