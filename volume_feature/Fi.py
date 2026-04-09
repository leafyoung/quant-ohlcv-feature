import pandas as pd


eps = 1e-8


def signal(*args):
    # Fi indicator (Force Index, z-score normalized with EMA smoothing)
    # Formula: FI = VOLUME * (CLOSE - REF(CLOSE, 1))
    #          FI_ZSCORE = (FI - MA(FI,N)) / STD(FI,N); result = EMA(FI_ZSCORE, N)
    # Force Index quantifies buying/selling force by combining price change magnitude with volume.
    # Z-score normalization removes scale effects; EMA smoothing reduces noise.
    # Positive values indicate sustained upward force; negative values indicate downward force.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    _fi = df['volume'] * (df['close'] - df['close'].shift(1))
    _fi_zscore = (_fi - _fi.rolling(n, min_periods=1).mean()) / \
                 (_fi.rolling(n, min_periods=1).std() + eps)
    s = _fi_zscore.ewm(span=n, adjust=False, min_periods=1).mean()
    df[factor_name] = pd.Series(s)

    return df
