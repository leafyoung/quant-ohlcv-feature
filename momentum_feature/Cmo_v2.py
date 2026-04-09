import numpy as np


eps = 1e-8


def signal(*args):
    # Cmo_v2 indicator (CMO variant using rolling max instead of sum)
    # Formula: CMO_v2 = (MAX(up_diff, N) - MAX(|dn_diff|, N)) / (MAX(up_diff, N) + MAX(|dn_diff|, N))
    # A variant of the Chande Momentum Oscillator that uses the rolling maximum of up/down moves
    # instead of their sum, making it more sensitive to extreme price swings.
    # Range: [-1, 1]. Positive = upside momentum; negative = downside momentum.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['momentum'] = df['close'] - df['close'].shift(1)
    df['up'] = np.where(df['momentum'] > 0, df['momentum'], 0)
    df['dn'] = np.where(df['momentum'] < 0, abs(df['momentum']), 0)
    df['up_sum'] = df['up'].rolling(window=n, min_periods=1).max()
    df['dn_sum'] = df['dn'].rolling(window=n, min_periods=1).max()
    df[factor_name] = (df['up_sum'] - df['dn_sum']) / (df['up_sum'] + df['dn_sum'] + eps)

    # delete extra columns
    del df['momentum'], df['up'], df['dn'], df['up_sum'], df['dn_sum']

    return df
