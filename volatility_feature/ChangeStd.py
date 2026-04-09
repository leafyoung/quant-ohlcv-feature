def signal(*args):
    # ChangeStd indicator (N-period return × rolling return std)
    # Formula: RTN = CLOSE.pct_change(); result = CLOSE.pct_change(N) * STD(RTN, N)
    # Combines directional momentum (N-period return) with recent volatility (rolling std of 1-period returns).
    # Acts as a risk-adjusted momentum measure: large returns in high-volatility environments are discounted.
    df = args[0]
    n = args[1]
    factor_name = args[2]
    
    rtn = df['close'].pct_change()
    df[factor_name] = df['close'].pct_change(n) * rtn.rolling(n).std(ddof=0)

    return df
