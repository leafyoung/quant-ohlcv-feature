import numpy as np
import pandas as pd


# ===== Function: 0-1 normalization
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
            1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)


def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # ******************** Nvi ********************
    # --- NVI --- 099/125
    # N=144
    # NVI_INC=IF(VOLUME<REF(VOLUME,1),1+(CLOSE-REF(CLOSE,1))/CLOSE,1)
    # NVI_INC[0]=100
    # NVI=CUM_PROD(NVI_INC)
    # NVI_MA=MA(NVI,N)
    # NVI is the cumulative percentage price change on days when volume decreases. NVI theory holds that
    # if prices rise while volume shrinks, it indicates large players are dominating the market.
    # NVI can be used to identify markets dominated by large players (price up, volume down).
    # A buy signal is generated when NVI crosses above NVI_MA;
    # a sell signal is generated when NVI crosses below NVI_MA.

    nvi_inc = np.where(df['volume'] < df['volume'].shift(1),
                       1 + (df['close'] - df['close'].shift(1)) / (1e-9 + df['close']), 1)
    nvi_inc[0] = 100
    nvi = pd.Series(nvi_inc).cumprod()
    nvi_ma = nvi.rolling(n, min_periods=1).mean()

    s = nvi - nvi_ma
    df[factor_name] = scale_01(s, n)

    return df
