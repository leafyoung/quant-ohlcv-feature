eps = 1e-8


def signal(*args):
    # KdjJ indicator (KDJ J line)
    # Formula: RSV = (CLOSE - MIN(LOW,N)) / (MAX(HIGH,N) - MIN(LOW,N)) * 100
    #          K = EWM(RSV, com=2); D = EWM(K, com=2); J = 3K - 2D
    # The J line of KDJ amplifies divergence between K and D lines.
    # J can exceed [0, 100] and is more sensitive to reversals than K or D alone.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    low_list = df['low'].rolling(n, min_periods=1).min()  # MIN(LOW,N) find minimum low within the period
    high_list = df['high'].rolling(n, min_periods=1).max()  # MAX(HIGH,N) find maximum high within the period
    # Stochastics=(CLOSE-LOW_N)/(HIGH_N-LOW_N)*100 calculate a stochastic value
    rsv = (df['close'] - low_list) / (high_list - low_list + eps) * 100
    # K D J values are within a fixed range
    df['K'] = rsv.ewm(com=2).mean()  # K=SMA(Stochastics,3,1) calculate K
    df['D'] = df['K'].ewm(com=2).mean()  # D=SMA(K,3,1) calculate D
    df[factor_name] = 3 * df['K'] - 2 * df['D']  # calculate J

    # remove redundant columns
    del df['K'], df['D']

    return df
