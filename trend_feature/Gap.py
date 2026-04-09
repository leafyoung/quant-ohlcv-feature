import talib as ta


def signal(*args):
    # GAP indicator (WMA vs MA normalized gap)
    # Formula: MA = MA(CLOSE,N); WMA = WMA(CLOSE,N); GAP = WMA - MA
    #          result = GAP / SUM(|GAP|, N)
    # Measures the directional gap between weighted and simple moving averages, normalized by its own magnitude sum.
    # Positive values indicate WMA > MA (recent prices stronger than average, upward momentum); negative when reversed.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['_ma'] = df['close'].rolling(window=n, min_periods=1).mean()
    df['_wma'] = ta.WMA(df['close'], n)
    df['_gap'] = df['_wma'] - df['_ma']
    df[factor_name] = (df['_gap'] / abs(df['_gap']).rolling(window=n).sum())

    del df['_ma']
    del df['_wma']
    del df['_gap']

    return df
