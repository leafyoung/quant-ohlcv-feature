def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # BOP indicator
    """
    N=20
    BOP=MA((CLOSE-OPEN)/(HIGH-LOW),N)
    BOP ranges from -1 to 1 and measures the ratio of the distance (positive or negative)
    between close and open prices to the distance between high and low prices, reflecting the
    bull/bear power balance in the market.
    If BOP>0, bulls have more advantage; BOP<0 means bears dominate. The larger the BOP,
    the more the price has been pushed toward the high; the smaller the BOP, the more
    the price has been pushed toward the low. We can use BOP crossing above/below 0 to generate buy/sell signals.
    """
    df['co'] = df['close'] - df['open']
    df['hl'] = df['high'] - df['low']
    df[factor_name] = (df['co'] / df['hl']).rolling(n, min_periods=1).mean()

    del df['co']
    del df['hl']

    return df
