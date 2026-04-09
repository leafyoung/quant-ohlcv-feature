eps = 1e-8


def signal(*args):
    # Sroc
    df = args[0]
    n = args[1]
    factor_name = args[2]
    
    """
    N=13
    M=21
    EMAP=EMA(CLOSE,N)
    SROC=(EMAP-REF(EMAP,M))/REF(EMAP,M)
    SROC is similar to ROC, but smooths the closing price before computing the rate of change.
    """
    ema = df['close'].ewm(n, adjust=False).mean()
    ref = ema.shift(2 * n)
    df[factor_name] = (ema - ref) / (ref + eps)

    return df
