eps = 1e-8


def signal(*args):
    # Hma
    df = args[0]
    n = args[1]
    factor_name = args[2]

    '''
    N=20
    HMA=MA(HIGH,N)
    The HMA indicator is a simple moving average where the close price is replaced by the high price.
    A buy/sell signal is generated when the high price crosses above/below HMA.
    '''
    hma = df['high'].rolling(n, min_periods=1).mean()
    # normalize (remove units)
    df[factor_name] = (df['high'] - hma) / (hma + eps)

    return df
