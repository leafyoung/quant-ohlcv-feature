import pandas as pd


# ===== function: zscore normalization
def scale_zscore(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).mean()
          ) / pd.Series(_s).rolling(_n, min_periods=1).std()
    return pd.Series(_s)


def signal(*args):
    # DzcciLowerSignal indicator (CCI Bollinger Lower band - Close, z-score normalized)
    # Formula: CCI = (TP - MA(TP,N)) / (0.015 * MD(TP,N)) where TP=(H+L+C)/3
    #          CCI_LOWER = MA(CCI,N) - 2*STD(CCI,N); result = ZSCORE(CCI_LOWER - CLOSE, N)
    # Measures how far the CCI lower Bollinger band is below the current close, z-score normalized.
    # Positive values suggest close is above the CCI lower band; negative values suggest oversold conditions.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    tp = df[['high', 'low', 'close']].sum(axis=1) / 3.
    ma = tp.rolling(n, min_periods=1).mean()
    md = (tp - ma).abs().rolling(n, min_periods=1).mean()
    cci = (tp - ma) / (1e-9 + 0.015 * md)
    cci_middle = pd.Series(cci).rolling(n, min_periods=1).mean()
    cci_lower = cci_middle - 2 * pd.Series(cci).rolling(n, min_periods=1).std()

    s = cci_lower - df['close']
    df[factor_name] = scale_zscore(s, n)

    return df
