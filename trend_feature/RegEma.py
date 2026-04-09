import talib as ta


eps = 1e-8


def signal(*args):
    # RegEma indicator (Close vs linear regression of EMA)
    # Formula: EMA = EMA(CLOSE, N); REG_EMA = LINEARREG(EMA, N); result = CLOSE / REG_EMA - 1
    # Measures deviation of close from the linear regression trend fitted to the EMA.
    # EMA smoothing reduces noise in the regression; the resulting signal shows how far close
    # strays from the smooth trend line.
    df = args[0]
    n = args[1]
    factor_name = args[2]
    
    ema = df['close'].ewm(span=n, adjust=False, min_periods=1).mean()
    reg_close = ta.LINEARREG(ema, timeperiod=n)
    df[factor_name] = df['close'] / (reg_close + eps) - 1

    return df
