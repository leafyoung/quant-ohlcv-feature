import numpy as np
import pandas as pd


def signal(*args):
    # Rwi indicator (Random Walk Index composite)
    # Formula: ATR = MA(TR, N)
    #          RWIH = (HIGH - REF(LOW,1)) / (SQRT(N) * ATR)   (upward RWI)
    #          RWIL = (REF(HIGH,1) - LOW) / (SQRT(N) * ATR)   (downward RWI)
    #          result = (CLOSE - RWIL) / (RWIH - RWIL)
    # The Random Walk Index measures whether price movement is beyond random (greater than 1 = trending).
    # This composite normalizes the close within the [RWIL, RWIH] range, giving a [0,1]-like score.
    df = args[0]
    n = args[1]
    factor_name = args[2]
    
    tr = np.max(np.array([
                (df['high'] - df['low']).abs(),
                (df['high'] - df['close'].shift(1)).abs(),
                (df['close'].shift(1) - df['low']).abs()
                ]), axis=0)  # take the maximum of the three series

    atr = pd.Series(tr).rolling(n, min_periods=1).mean()
    _rwih = (df['high'] - df['low'].shift(1)) / (np.sqrt(n) * atr)
    _rwil = (df['high'].shift(1) - df['low']) / (np.sqrt(n) * atr)

    _rwi = (df['close'] - _rwil) / (1e-9 + _rwih - _rwil)
    df[factor_name] = pd.Series(_rwi)

    return df
