eps = 1e-8


def signal(*args):
    # BbiBias
    df = args[0]
    n = args[1]
    factor_name = args[2]

    """
    BBI=(MA(CLOSE,3)+MA(CLOSE,6)+MA(CLOSE,12)+MA(CLOSE,24))/4
    BBI averages moving averages of different lengths, combining the smoothness and lag
    of different moving averages. A buy/sell signal is generated when the close crosses above/below BBI.
    """
    # calculate BBI indicator to compute bias
    ma1 = df['close'].rolling(n, min_periods=1).mean()
    ma2 = df['close'].rolling(2 * n, min_periods=1).mean()
    ma3 = df['close'].rolling(4 * n, min_periods=1).mean()
    ma4 = df['close'].rolling(8 * n, min_periods=1).mean()
    # BBI=(MA(CLOSE,3)+MA(CLOSE,6)+MA(CLOSE,12)+MA(CLOSE,24))/4
    bbi = (ma1 + ma2 + ma3 + ma4) / 4
    df[factor_name] = df['close'] / (bbi + eps) - 1

    return df
