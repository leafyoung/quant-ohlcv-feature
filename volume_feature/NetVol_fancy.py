import numpy as np


def signal(*args):
    # Quote volume weighted by the sign of returns, simulating net capital inflow/outflow
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['_ret_sign'] = np.sign(df['close'].pct_change())
    df[factor_name] = (df['_ret_sign'] * df['quote_volume']).rolling(n, min_periods=1).sum()

    del df['_ret_sign']

    return df
