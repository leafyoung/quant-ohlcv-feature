def signal(*args):
    df = args[0]
    n  = args[1]
    factor_name = args[2]

    # WR indicator
    """
    HIGH(N)=MAX(HIGH,N)
    LOW(N)=MIN(LOW,N)
    WR=100*(HIGH(N)-CLOSE)/(HIGH(N)-LOW(N))
    WR is essentially 100 minus the Stochastics used in KDJ calculation.
    WR measures market strength and overbought/oversold conditions.
    Generally, WR < 20 indicates an overbought market; WR > 80 indicates an oversold market;
    WR between 20 and 80 indicates a relatively balanced market.
    A buy signal is generated when WR crosses above 80;
    a sell signal is generated when WR crosses below 20.
    """
    df['max_high'] = df['high'].rolling(n, min_periods=1).max()
    df['min_low'] = df['low'].rolling(n, min_periods=1).min()
    df[factor_name] = (df['max_high'] - df['close']) / (df['max_high'] - df['min_low']) * 100
    
    del df['max_high']
    del df['min_low']

    return df
