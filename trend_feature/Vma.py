eps = 1e-8


def signal(*args):
    # Vma
    df = args[0]
    n = args[1]
    factor_name = args[2]

    """
    N=20
    PRICE=(HIGH+LOW+OPEN+CLOSE)/4
    VMA=MA(PRICE,N)
    VMA is simply a moving average that replaces the close price with the average of
    high, low, open and close. A buy/sell signal is generated when PRICE crosses above/below VMA.
    """
    price = (df['high'] + df['low'] + df['open'] + df['close']) / 4  # PRICE=(HIGH+LOW+OPEN+CLOSE)/4
    vma = price.rolling(n, min_periods=1).mean()  # VMA=MA(PRICE,N)
    df[factor_name] = price / (vma + eps) - 1  # normalize

    return df
