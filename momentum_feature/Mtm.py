def signal(*args):
    # Mtm indicator (Simple N-period momentum)
    # Formula: MTM = (CLOSE / REF(CLOSE, N) - 1) * 100
    # Measures the percentage price change over N periods. Positive values indicate upward momentum.
    # The most basic momentum indicator; useful as a building block for composite factors.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = (df['close'] / df['close'].shift(n) - 1) * 100

    return df
