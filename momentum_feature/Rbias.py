def signal(*args):
    # Rbias indicator (Rate of change of Bias)
    # Formula: BIAS = CLOSE / MA(CLOSE, N); result = BIAS / REF(BIAS, 1) - 1
    # Measures the 1-period change in the price-to-MA ratio, i.e., how fast the bias is growing or shrinking.
    # Positive values indicate bias is increasing (price diverging further from MA upward).
    df = args[0]
    n = args[1]
    factor_name = args[2]
    
    ma = df['close'].rolling(n, min_periods=1).mean()
    df[factor_name] = (df['close'] / ma) / (df['close'].shift(1) / ma.shift(1)) - 1

    return df
