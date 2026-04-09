def signal(*args):
    # PmoTema indicator (PMO using TEMA instead of CLOSE)
    # Formula: TEMA = 3*EMA - 3*EMA(EMA) + EMA(EMA(EMA))
    #          ROC = (TEMA - REF(TEMA,1)) / REF(TEMA,1) * 100
    #          PMO_TEMA = MA(MA(ROC,N)*10, 4N) smoothed by MA(2N)
    # A Price Momentum Oscillator computed on the Triple EMA (TEMA) instead of close price.
    # TEMA reduces lag; the double smoothing of ROC produces a slow, signal-line-like oscillator.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # TEMA moving average
    df['ema'] = df['close'].ewm(n, adjust=False).mean()
    df['ema_ema'] = df['ema'].ewm(n, adjust=False).mean()
    df['ema_ema_ema'] = df['ema_ema'].ewm(n, adjust=False).mean()
    df['TEMA'] = 3 * df['ema'] - 3 * df['ema_ema'] + df['ema_ema_ema']

    # calculate PMO
    df['ROC'] = (df['TEMA'] - df['TEMA'].shift(1)) / \
        df['TEMA'].shift(1) * 100  # use TEMA moving average instead of original CLOSE
    df['ROC_MA'] = df['ROC'].rolling(
        n, min_periods=1).mean()  # use moving average instead of dynamic moving average
    df['ROC_MA10'] = df['ROC_MA'] * 10
    df['PMO'] = df['ROC_MA10'].rolling(4 * n, min_periods=1).mean()
    df[factor_name] = df['PMO'].rolling(2 * n, min_periods=1).mean()

    del df['ema'], df['ema_ema'], df['ema_ema_ema'], df['TEMA']
    del df['ROC'], df['ROC_MA']
    del df['ROC_MA10']
    del df['PMO']

    return df
