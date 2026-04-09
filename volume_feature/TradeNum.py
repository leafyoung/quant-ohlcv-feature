def signal(*args):
    # TradeNum indicator
    # Formula: result = SUM(trade_num, N)
    # Rolling sum of the number of trades over N periods. A proxy for market activity and liquidity.
    # Higher values indicate more transactions occurring, often associated with increased market interest.
    df = args[0]
    n = args[1]
    factor_name = args[2]
    
    df[factor_name] = df['trade_num'].rolling(n, min_periods=1).sum()

    return df
