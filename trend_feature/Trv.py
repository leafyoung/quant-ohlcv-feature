def signal(*args):
    # Trv indicator (Rolling percentage change of Moving Average)
    # Formula: MA = MA(CLOSE,N); TRV = 100 * (MA - REF(MA,N)) / REF(MA,N)
    #          result = MA(TRV, N)
    # Measures the smoothed N-period rate of change of the moving average.
    # Captures the velocity of the trend rather than the raw price movement.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # calculate volatility factor
    df['ma'] = df['close'].rolling(window=n, min_periods=1).mean()
    df['trv'] = 100 * ((df['ma'] - df['ma'].shift(n)) / df['ma'].shift(n))
    df[factor_name] = df['trv'].rolling(n, min_periods=1).mean()

    drop_col = [
       'ma', 'trv'
    ]
    df.drop(columns=drop_col, inplace=True)

    return df
