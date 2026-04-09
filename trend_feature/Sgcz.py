eps = 1e-8


def signal(*args):
    # Sgcz indicator (Close vs rolling mean of High)
    # Formula: HIGH_MA = MA(HIGH, N); result = (CLOSE - HIGH_MA) / (HIGH_MA + eps)
    # Measures how far the close price is below the rolling average high.
    # Negative values (typical) indicate close is below average high; values near 0 suggest close is near the high mean.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    high = df['high'].rolling(n, min_periods=1).mean()
    close = df['close']
    df[factor_name] = (close - high) / (high + eps)

    return df
