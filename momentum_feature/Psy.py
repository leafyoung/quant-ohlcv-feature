import numpy as np


def signal(*args):
    # Psy
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['P'] = np.where(df['close'] > df['close'].shift(1), 1, 0)  # IF(CLOSE>REF(CLOSE,1),1,0)
    df[factor_name] = df['P'].rolling(n, min_periods=1).sum() / n * 100  # PSY=IF(CLOSE>REF(CLOSE,1),1,0)/N*100

    # delete extra columns
    del df['P']

    return df
