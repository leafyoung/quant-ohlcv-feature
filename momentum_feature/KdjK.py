eps = 1e-8


def signal(*args):
    # KdjK indicator (KDJ K line)
    # Formula: RSV = (CLOSE - MIN(LOW,N)) / (MAX(HIGH,N) - MIN(LOW,N)) * 100
    #          K = EWM(RSV, com=2)
    # The K line of the KDJ oscillator — smoothed stochastic value.
    # Measures where the close is within the N-period high-low range, smoothed once.
    # Overbought > 80; oversold < 20.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    low_list = df['low'].rolling(n, min_periods=1).min()  # MIN(LOW,N) find minimum low within the period
    high_list = df['high'].rolling(n, min_periods=1).max()  # MAX(HIGH,N) find maximum high within the period
    # Stochastics=(CLOSE-LOW_N)/(HIGH_N-LOW_N)*100 calculate a stochastic value
    rsv = (df['close'] - low_list) / (high_list - low_list + eps) * 100
    # K D J values are within a fixed range
    df[factor_name] = rsv.ewm(com=2).mean()  # K=SMA(Stochastics,3,1) calculate K

    return df
