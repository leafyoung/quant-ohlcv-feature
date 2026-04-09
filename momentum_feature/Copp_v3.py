# Copp_v3 by zhengk
def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # COPP indicator
    """
    RC=100*((CLOSE-REF(CLOSE,N1))/REF(CLOSE,N1)+(CLOSE-REF(CLOSE,N2))/REF(CLOSE,N2))
    COPP=WMA(RC,M)
    The COPP indicator uses a weighted moving average of price rate-of-change over different time lengths to measure
    momentum. If COPP crosses above/below 0, it generates a buy/sell signal.
    """
    df['RC'] = 100 * ((df['close'] - df['close'].shift(n)) / df['close'].shift(n) + ( df['close'] - df['close'].shift(int(1.618 * n))) / df['close'].shift(int(1.618 * n)))
    df[factor_name] = df['RC'].rolling(n, min_periods=1).mean()

    del df['RC']

    return df
