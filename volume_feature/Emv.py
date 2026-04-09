import pandas as pd


def signal(*args):
    # Emv indicator (Ease of Movement)
    # Formula: MPM = (HIGH+LOW)/2 - REF((HIGH+LOW)/2, 1)  (midpoint move)
    #          BR = VOLUME / MA(VOLUME,N) / (HIGH - LOW)   (box ratio: volume density)
    #          EMV = MPM / BR
    # Measures how easily price moves, combining price midpoint change with the "box ratio"
    # (volume per unit of price range). High positive EMV indicates price rising with low volume
    # resistance; negative EMV indicates falling with low resistance.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    mpm = (df['high'] + df['low']) / 2. - \
        (df['high'].shift(1) + df['low'].shift(1)) / 2.
    v_divisor = df['volume'].rolling(n, min_periods=1).mean()
    _br = df['volume'] / v_divisor / (1e-9 + df['high'] - df['low'])

    s = mpm / (1e-9 + _br)
    df[factor_name] = pd.Series(s)

    return df
