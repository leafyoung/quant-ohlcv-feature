def signal(df, n, factor_name, config):
    # Dema indicator
    """
    N=60
    EMA=EMA(CLOSE,N)
    DEMA=2*EMA-EMA(EMA,N)
    DEMA combines single EMA and double EMA to reduce lag while maintaining smoothness.
    """
    ema = df["close"].ewm(span=n, adjust=config.ewm_adjust).mean()  # EMA=EMA(CLOSE,N)
    ema_ema = ema.ewm(span=n, adjust=config.ewm_adjust).mean()  # EMA(EMA,N)
    dema = 2 * ema - ema_ema  # DEMA=2*EMA-EMA(EMA,N)
    # normalize dema
    df[factor_name] = dema / (ema + config.eps) - 1

    return df
