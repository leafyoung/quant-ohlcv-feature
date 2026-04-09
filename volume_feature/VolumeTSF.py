import talib as ta


def signal(*args):
    # VolumeTSF indicator (Time Series Forecast of Quote Volume)
    # Formula: result = TSF(QUOTE_VOLUME, N)
    # Applies talib's Time Series Forecast (linear regression extrapolation) to quote volume.
    # Projects the volume trend one step ahead based on the linear regression over N periods.
    # Useful for estimating whether volume is trending up or down relative to recent history.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = ta.TSF(df['quote_volume'], timeperiod=n)

    return df
