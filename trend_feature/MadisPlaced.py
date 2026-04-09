def signal(*args):
    # Note: when using this indicator, n must not exceed half the number of filtered candles (not half the number of fetched candles)
    """
    N=20
    M=10
    MA_CLOSE=MA(CLOSE,N)
    MADisplaced=REF(MA_CLOSE,M)
    The MADisplaced indicator shifts the simple moving average forward by M trading days,
    and is used similarly to a regular moving average. Buy/sell signals are generated
    when the closing price crosses above/below MADisplaced.
    Somewhat similar to a variant of Bias.
    """
    df = args[0]
    n = args[1]
    factor_name = args[2]

    ma = df['close'].rolling(2 * n, min_periods=1).mean()  # MA(CLOSE,N) fix relationship between two parameters to reduce parameters
    ref = ma.shift(n)  # MADisplaced=REF(MA_CLOSE,M)

    df[factor_name] = df['close'] / ref - 1  # normalize

    return df
