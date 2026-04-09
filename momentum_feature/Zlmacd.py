def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # ZLMACD indicator
    """
    N1=20
    N2=100
    ZLMACD=(2*EMA(CLOSE,N1)-EMA(EMA(CLOSE,N1),N1))-(2*EM
    A(CLOSE,N2)-EMA(EMA(CLOSE,N2),N2))
    ZLMACD is an improvement on the MACD indicator that uses DEMA instead of EMA in its
    calculation, overcoming the lag of the MACD indicator. A buy/sell signal is generated
    when ZLMACD crosses above/below 0.
    """
    ema1 = df['close'].ewm(n, adjust=False).mean()
    ema_ema_1 = ema1.ewm(n, adjust=False).mean()
    n2 = 5 * n
    ema2 = df['close'].ewm(n2, adjust=False).mean()
    ema_ema_2 = ema2.ewm(n2, adjust=False).mean()
    ZLMACD = (2 * ema1 - ema_ema_1) - (2 * ema2 - ema_ema_2)
    df[factor_name] = df['close'] / ZLMACD - 1

    return df
