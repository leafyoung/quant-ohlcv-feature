eps = 1e-8


def signal(*args):
    # Cci_v3 indicator (CCI using all four OHLC EMA-smoothed prices)
    # Formula: TP = (EMA(O,N) + EMA(H,N) + EMA(L,N) + EMA(C,N)) / 4
    #          MA = EMA(TP, N); MD = EMA(|EMA(C,N) - MA|, N)
    #          result = (TP - MA) / (MD + eps)
    # A variant of CCI using all four OHLC prices EMA-smoothed as the typical price.
    # Uses EMA-based mean deviation for smoother response compared to standard CCI.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    oma = df['open'].ewm(span=n, adjust=False).mean()
    hma = df['high'].ewm(span=n, adjust=False).mean()
    lma = df['low'].ewm(span=n, adjust=False).mean()
    cma = df['close'].ewm(span=n, adjust=False).mean()
    tp = (oma + hma + lma + cma) / 4
    ma = tp.ewm(span=n, adjust=False).mean()
    md = (cma - ma).abs().ewm(span=n, adjust=False).mean()
    df[factor_name] = (tp - ma) / (md + eps)

    return df
