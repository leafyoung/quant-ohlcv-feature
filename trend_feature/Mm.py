eps = 1e-8


def signal(*args):
    # Mm indicator (Fast MA / Slow MA)
    # Formula: MA_FAST = MA(CLOSE, N); MA_SLOW = MA(CLOSE, 5N)
    #          result = MA_FAST / MA_SLOW - 1
    # Measures the relative divergence between a short and long moving average.
    # Positive values indicate short MA above long MA (uptrend); negative indicate downtrend.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    ma_fast = df['close'].rolling(n, min_periods=1).mean()
    ma_slow = df['close'].rolling(5*n, min_periods=1).mean()
    df[factor_name] = ma_fast / (ma_slow + eps) - 1

    return df
