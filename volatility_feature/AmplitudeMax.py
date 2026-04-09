import numpy as np


def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # AmplitudeMax indicator (Rolling maximum candle amplitude)
    # Formula: AMPLITUDE = MAX(|HIGH/OPEN - 1|, |LOW/OPEN - 1|); result = ROLLING_MAX(AMPLITUDE, N)
    # Measures the maximum single-candle price swing (as a fraction of open) over N periods.
    # Captures the largest intrabar move, useful for detecting outlier volatility events.
    df['hourly_amplitude'] = np.maximum(
        abs(df['high'] / df['open'] - 1),
        abs(df['low'] / df['open'] - 1)
    )
    df[factor_name] = df['hourly_amplitude'].rolling(n).max()
    del df['hourly_amplitude']

    return df
