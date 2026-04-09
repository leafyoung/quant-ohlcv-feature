def signal(*args):
    # Roc indicator (Simple N-period Rate of Change)
    # Formula: ROC = CLOSE / REF(CLOSE, N) - 1
    # Measures the proportional price change over N periods (similar to Mtm but without ×100).
    # Positive values indicate upward movement; negative indicate downward movement.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = df['close'] / df['close'].shift(n) - 1

    return df
