def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # CciMagic indicator (Modified CCI using MA of OHLC prices)
    # Formula: TP = (MA(HIGH,N) + MA(LOW,N) + MA(CLOSE,N)) / 3
    #          MA_TP = MA(TP, N); MD = MA(|MA_TP - MA(CLOSE,N)|, N)
    #          result = (TP - MA_TP) / (0.015 * MD)
    # A smoothed CCI variant where both H, L, C are first averaged over N periods before computing CCI.
    # This reduces noise compared to standard CCI computed on raw prices.

    # calculate modified CCI indicator
    open_ma = df['open'].rolling(n, min_periods=1).mean()
    high_ma = df['high'].rolling(n, min_periods=1).mean()
    low_ma = df['low'].rolling(n, min_periods=1).mean()
    close_ma = df['close'].rolling(n, min_periods=1).mean()
    tp = (high_ma + low_ma + close_ma) / 3
    ma = tp.rolling(n, min_periods=1).mean()
    md = abs(ma - close_ma).rolling(n, min_periods=1).mean()
    df[factor_name] = ((tp - ma) / md / 0.015)

    return df
