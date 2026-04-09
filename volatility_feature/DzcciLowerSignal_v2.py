import pandas as pd


# ===== function: 0-1 normalization
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)


def signal(*args):
    # DzcciLowerSignal_v2 indicator (CCI Bollinger Lower band - CCI short MA, 0-1 normalized)
    # Formula: CCI = (TP - MA(TP,N)) / (0.015 * MD(TP,N)) where TP=(H+L+C)/3
    #          CCI_LOWER = MA(CCI,N) - 2*STD(CCI,N); CCI_MA = MA(CCI, N/4)
    #          result = scale_01(CCI_LOWER - CCI_MA, N)
    # Measures how far the CCI lower band is below the short-term CCI MA, normalized to [0,1].
    # Low values indicate CCI is compressed near or above its lower band; high values suggest expansion downward.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    tp = df[['high', 'low', 'close']].sum(axis=1) / 3.
    ma = tp.rolling(n, min_periods=1).mean()
    md = (tp - ma).abs().rolling(n, min_periods=1).mean()
    cci = (tp - ma) / (1e-9 + 0.015 * md)
    cci_middle = pd.Series(cci).rolling(n, min_periods=1).mean()
    cci_lower = cci_middle - 2 * pd.Series(cci).rolling(n, min_periods=1).std()
    cci_ma = pd.Series(cci).rolling(max(1, int(n / 4)), min_periods=1).mean()

    s = cci_lower - cci_ma
    df[factor_name] = scale_01(s, n)

    return df
