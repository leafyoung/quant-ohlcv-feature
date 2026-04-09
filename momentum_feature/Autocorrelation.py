def signal(*args):
    # Return Autocorrelation (lag-1 rolling autocorrelation of returns)
    # Formula: RETURN = (CLOSE - CLOSE.shift(1)) / CLOSE.shift(1)
    #          result = ROLLING_CORR(RETURN, RETURN.shift(1), N)
    # Measures the persistence of returns over the past N periods.
    # Positive values indicate momentum (trending), negative values indicate mean-reversion.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['_return'] = df['close'].pct_change()
    df['_return_lag1'] = df['_return'].shift(1)

    df[factor_name] = df['_return'].rolling(n, min_periods=2).corr(df['_return_lag1'])

    del df['_return']
    del df['_return_lag1']

    return df