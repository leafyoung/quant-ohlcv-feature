import talib as ta


eps = 1e-8


def signal(*args):
    # Tema_v2 indicator (Close vs longer-period TEMA, percentage)
    # Formula: TEMA = TEMA(CLOSE, 2N); result = 100 * (CLOSE - TEMA) / (TEMA + eps)
    # Measures the percentage deviation of close from its 2N-period Triple Exponential MA.
    # Uses a longer window (2N) than the standard TEMA for a smoother trend baseline.
    # Positive values indicate close is above TEMA (upward momentum); negative below.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['TEMA'] = ta.TEMA(df['close'], timeperiod=2 * n)
    df[factor_name] = 100 * (df['close'] - df['TEMA']) / (df['TEMA'] + eps)

    del df['TEMA']

    return df
