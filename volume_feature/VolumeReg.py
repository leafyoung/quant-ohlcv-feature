import talib as ta


def signal(*args):
    # VolumeReg indicator (Linear Regression of Quote Volume)
    # Formula: result = LINEARREG(QUOTE_VOLUME, N)
    # Fits a linear regression to quote volume over N periods and returns the regression value.
    # Captures the trend direction and level of trading volume, smoothing out short-term noise.
    # Rising values indicate volume is trending up; falling values indicate declining volume trend.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = ta.LINEARREG(df['quote_volume'], timeperiod=n)

    return df
