import talib as ta


eps = 1e-8


def signal(*args):
    # Sroc_v2 indicator (KAMA-based Smoothed Rate of Change)
    # Formula: KAMA = KAMA(CLOSE, N); result = (KAMA - REF(KAMA, 2N)) / REF(KAMA, 2N)
    # Computes the rate of change of the Kaufman Adaptive Moving Average (KAMA) over 2N periods.
    # KAMA adapts to volatility, so SROC_v2 gives a momentum signal that is less sensitive to noise.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    ema = ta.KAMA(df['close'], n)
    ref = ema.shift(2 * n)
    df[factor_name] = (ema - ref) / (ref + eps)

    return df
