
# LowPrice indicator (rolling mean close price — low-priced asset factor)
# Formula: result = MA(CLOSE, N)
# Returns the raw N-period moving average of close price as a factor.
# Used to identify low-priced assets; lower values indicate cheaper assets relative to history.
def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = df['close'].rolling(n, min_periods=1).mean()

    return df


def signal_multi_params(df, param_list) -> dict:
    """
    Use multi-parameter aggregated computation for the same factor to significantly speed
    up backtesting and live cal_factor calls — approximately 3x faster than `signal`.
    :param df: dataframe of candlestick data
    :param param_list: list of parameters
    """
    ret = dict()
    for param in param_list:
        n = int(param)
        ret[str(param)] = df['close'].rolling(n, min_periods=1).mean()
    return ret
