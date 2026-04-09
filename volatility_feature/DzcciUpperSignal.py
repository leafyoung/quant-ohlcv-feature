import pandas as pd


# ===== function: 0-1 normalization
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)


def signal(*args):
    # DzcciUpperSignal indicator (Close - CCI Bollinger Upper band, 0-1 normalized)
    # Formula: CCI = (TP - MA(TP,N)) / (0.015 * MD(TP,N)) where TP=(H+L+C)/3
    #          CCI_UPPER = MA(CCI,N) + 2*STD(CCI,N); result = scale_01(CLOSE - CCI_UPPER, N)
    # Measures how far the close price is above the CCI upper Bollinger band.
    # Positive signal values indicate close is breaking above the upper band (overbought or breakout signal).
    df = args[0]
    n = args[1]
    factor_name = args[2]

    tp = df[['high', 'low', 'close']].sum(axis=1) / 3.
    ma = tp.rolling(n, min_periods=1).mean()
    md = (tp - ma).abs().rolling(n, min_periods=1).mean()
    cci = (tp - ma) / (1e-9 + 0.015 * md)
    cci_middle = pd.Series(cci).rolling(n, min_periods=1).mean()
    cci_upper = cci_middle + 2 * pd.Series(cci).rolling(n, min_periods=1).std()

    s = df['close'] - cci_upper
    df[factor_name] = scale_01(s, n)

    return df
