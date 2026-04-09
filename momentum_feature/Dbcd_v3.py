import pandas as pd


def sma(ser: pd.Series, n, m=1) -> list:
    ser.fillna(value=0, inplace=True)
    # SMA(X,N,M) = M/N*X+(N-M)/N*REF(SMA,1)
    _l = []
    for i, v in enumerate(ser):
        if i == 0:
            _l.append(v)
        else:
            r = m / n
            _l.append(r * v + (1 - r) * _l[-1])

    return _l


def signal(*args):
    # Dbcd_v3 indicator
    '''
    N=5
    M=16
    T=17
    BIAS=(CLOSE-MA(CLOSE,N)/MA(CLOSE,N))*100
    BIAS_DIF=BIAS-REF(BIAS,M)
    DBCD=SMA(BIAS_DIFF,T,1)
    DBCD (Divergence of Bias) is the moving average of bias divergence.
    We use DBCD crossing above 5% / crossing below -5% to generate buy/sell signals.
    '''
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['ma'] = df['close'].rolling(n, min_periods=1).mean()
    df['BIAS'] = (df['close'] - df['ma']) / df['ma'] * 100
    df['BIAS_DIF'] = df['BIAS'] - df['BIAS'].shift(3 * n)
    t = 3 * n + 2
    df[factor_name] = sma(df['BIAS_DIF'], t, 1)

    del df['ma']
    del df['BIAS']
    del df['BIAS_DIF']

    return df
