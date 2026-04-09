def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]
    # TYP indicator
    """
    N1=10
    N2=30
    TYP=(CLOSE+HIGH+LOW)/3
    TYPMA1=EMA(TYP,N1)
    TYPMA2=EMA(TYP,N2)
    In technical analysis, the typical price (high + low + close) / 3 is often used
    instead of the closing price. For example, when generating signals from MA crossings,
    we can use the moving average of the typical price.
    Buy/sell signals are generated when TYPMA1 crosses above/below TYPMA2.
    """
    TYP = (df['close'] + df['high'] + df['low']) / 3
    TYPMA1 = TYP.ewm(n, adjust=False).mean()
    TYPMA2 = TYP.ewm(n * 3, adjust=False).mean()
    diff_TYP = TYPMA1 - TYPMA2
    diff_TYP_mean = diff_TYP.rolling(n, min_periods=1).mean()
    diff_TYP_std = diff_TYP.rolling(n, min_periods=1).std()

    # normalize
    df[factor_name] = diff_TYP - diff_TYP_mean / diff_TYP_std

    return df
