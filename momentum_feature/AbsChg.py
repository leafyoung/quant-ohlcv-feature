def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # AbsChg indicator (Absolute N-period price change)
    # Formula: result = |CLOSE.pct_change(N)|
    # Measures the absolute magnitude of the N-period return regardless of direction.
    # High values indicate significant price moves; useful as a volatility proxy or for filtering signals.
    df[factor_name] = abs(df['close'].pct_change(n))

    return df
