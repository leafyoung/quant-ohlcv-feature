import pandas as pd


# ===== Function: 0-1 normalization
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)


def signal(*args):
    # EnvLower
    df = args[0]
    n = args[1]
    factor_name = args[2]

    '''
    N=25
    PARAM=0.05
    MAC=MA(CLOSE,N)
    UPPER=MAC*(1+PARAM)
    LOWER=MAC*(1-PARAM)
    The ENV (Envelope) indicator is derived by shifting the moving average up and down by a certain percentage.
    Price crossovers with the moving average can generate trading signals.
    However, because the market itself is highly volatile, many false trading signals may be generated.
    Therefore, the moving average is shifted up and down.
    A buy signal is generated when price breaks through the upper band, and a sell signal when it breaks through the lower band.
    This approach can eliminate many false signals.
    '''

    lower = (1 - 0.05) * df['close'].rolling(n, min_periods=1).mean()

    s = lower
    df[factor_name] = scale_01(s, n)

    return df
