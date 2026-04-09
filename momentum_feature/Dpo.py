eps = 1e-8


def signal(*args):
    # Dpo
    df = args[0]
    n = args[1]
    factor_name = args[2]

    '''
    N=20
    DPO=CLOSE-REF(MA(CLOSE,N),N/2+1)
    DPO is the difference between the current price and a lagged moving average,
    reducing the influence of long-term trends on short-term price fluctuations by removing a prior moving average.
    DPO>0 indicates the current market is bullish;
    DPO<0 indicates the current market is bearish.
    We use DPO crossing above/below 0 to generate buy/sell signals.
    '''

    df['median'] = df['close'].rolling(window=n, min_periods=1).mean()  # calculate middle band
    df[factor_name] = (df['close'] - df['median'].shift(int(n / 2) + 1)) / (df['median'] + eps)

    del df['median']

    return df
