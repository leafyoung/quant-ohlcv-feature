def signal(*args):
    # VolumeStd indicator (Rolling standard deviation of quote volume)
    # Formula: result = STD(QUOTE_VOLUME, N)
    # Measures the dispersion of quote volume over N periods. Higher values indicate
    # more erratic volume activity (spikes and lulls); lower values indicate steady volume.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = df['quote_volume'].rolling(n, min_periods=2).std()

    return df
