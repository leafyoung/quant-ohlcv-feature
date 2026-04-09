def signal(*args):
    # POS indicator
    """
    N=100
    PRICE=(CLOSE-REF(CLOSE,N))/REF(CLOSE,N)
    POS=(PRICE-MIN(PRICE,N))/(MAX(PRICE,N)-MIN(PRICE,N))
    POS measures where the current N-day return falls between the maximum and minimum
    N-day returns over the past N days. A buy signal is generated when POS crosses above 80;
    a sell signal is generated when POS crosses below 20.

    """
    df = args[0]
    n = args[1]
    factor_name = args[2]

    ref = df['close'].shift(n)
    price = (df['close'] - ref) / ref
    min_price = price.rolling(n).min()
    max_price = price.rolling(n).max()
    df[factor_name] = (price - min_price) / (max_price - min_price)

    return df
