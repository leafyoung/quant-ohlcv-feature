import numpy as np


eps = 1e-8


def signal(*args):
    # Bias_v3 indicator (log-scale Bias normalized by 0.03)
    # Formula: MA = MA(CLOSE, N); result = log(CLOSE / (MA + eps)) / 0.03
    # Computes logarithmic deviation of close from its moving average, normalized by a fixed scale factor.
    # Positive values indicate close is above MA (upward bias); negative below.
    # Division by 0.03 normalizes the log-returns to a reasonable numeric range.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    ma = df['close'].rolling(n, min_periods=1).mean()
    # will output nan, / 0.03 to normalize data
    df[factor_name] = np.log((df['close'] / (ma + eps))) / 0.03

    return df
