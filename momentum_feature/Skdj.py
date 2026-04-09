def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # SKDJ indicator
    """
    N=60
    M=5
    RSV=(CLOSE-MIN(LOW,N))/(MAX(HIGH,N)-MIN(LOW,N))*100
    MARSV=SMA(RSV,3,1)
    K=SMA(MARSV,3,1)
    D=MA(K,3)
    SKDJ is the Slow Stochastic Oscillator (i.e., Slow KDJ). K in SKDJ corresponds to D in KDJ,
    and D in SKDJ is the moving average of D in KDJ. Usage is the same as KDJ.
    Buy when D < 40 (oversold) and K crosses above D; sell when D > 60 (overbought) and K crosses below D.
    """
    df['RSV'] = (df['close'] - df['low'].rolling(n, min_periods=1).min()) / (df['high'].rolling(n, min_periods=1).max() - df['low'].rolling(n, min_periods=1).min()) * 100
    df['MARSV'] = df['RSV'].ewm(com=2).mean()

    df['K'] = df['MARSV'].ewm(com=2).mean()
    df[factor_name] = df['K'].rolling(3, min_periods=1).mean()
    
    del df['RSV']
    del df['MARSV']
    del df['K']

    return df
