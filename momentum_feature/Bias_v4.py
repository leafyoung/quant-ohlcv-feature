eps = 1e-8


def signal(*args):
    # Bias_v4 indicator (Typical price bias from MA)
    # Formula: TP = (HIGH + LOW + CLOSE) / 3; result = TP / MA(TP, N) - 1
    # Uses the typical price (HLC/3) instead of close to compute the bias from MA.
    # More representative of the full candle range than close-only bias.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    ts = df[['high', 'low', 'close']].sum(axis=1) / 3.
    ma = ts.rolling(n, min_periods=1).mean()
    df[factor_name] = ts / (ma + eps) - 1

    return df
