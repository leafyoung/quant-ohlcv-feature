def signal(*args):
    # Clv indicator
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # CLV=(2*CLOSE-LOW-HIGH)/(HIGH-LOW)
    df['CLV'] = (2 * df['close'] - df['low'] - df['high']) / (df['high'] - df['low'])
    df[factor_name] = df['CLV'].rolling(n, min_periods=1).mean()  # CLVMA=MA(CLV,N)

    # delete extra columns
    del df['CLV']

    return df
