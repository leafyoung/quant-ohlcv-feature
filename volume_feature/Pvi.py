import numpy as np


def signal(*args):
    # PVI indicator
    """
    N=40
    PVI_INC=IF(VOLUME>REF(VOLUME,1),(CLOSE-REF(CLOSE))/
    CLOSE,0)
    PVI=CUM_SUM(PVI_INC)
    PVI_MA=MA(PVI,N)
    PVI is the cumulative percentage price change on days when volume increases.
    PVI theory holds that rising prices with increasing volume indicates retail investors
    are dominating the market. PVI can be used to identify such markets.
    A buy signal is generated when PVI crosses above PVI_MA;
    a sell signal is generated when PVI crosses below PVI_MA.
    """
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['ref_close'] = (df['close'] - df['close'].shift(1)) / df['close']
    df['PVI_INC'] = np.where(df['volume'] > df['volume'].shift(1), df['ref_close'], 0)
    df['PVI'] = df['PVI_INC'].cumsum()
    df[factor_name] = df['PVI'].rolling(n, min_periods=1).mean()

    del df['ref_close']
    del df['PVI_INC']
    del df['PVI']

    return df
