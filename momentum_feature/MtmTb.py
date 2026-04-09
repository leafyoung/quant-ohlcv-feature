def signal(*args):
    # MtmTb indicator (Momentum mean × Taker buy ratio)
    # Formula: MTM_MEAN = EMA(CLOSE/REF(CLOSE,N)-1, N)
    #          TAKER_BUY_MA = MA(taker_buy_quote / MA(quote_volume,N) * 100, N)
    #          result = MTM_MEAN * TAKER_BUY_MA
    # Multiplies EMA-smoothed price momentum by the average taker buy pressure (as % of volume).
    # High positive values indicate strong upside momentum backed by buyer-initiated trades.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # df['tr_trix'] = df['close'].ewm(span=n, adjust=False).mean()
    # df['tr_pct'] = df['tr_trix'].pct_change()
    # average taker buy ratio
    df['MtmMean'] = (df['close'] / df['close'].shift(n) - 1).ewm(n, adjust=False).mean()
    df['vma'] = df['quote_volume'].rolling(n, min_periods=1).mean()
    df['taker_buy_ma'] = (df['taker_buy_quote_asset_volume'] / df['vma']) * 100
    df['taker_buy_mean'] = df['taker_buy_ma'].rolling(window=n).mean()

    df[factor_name] = df['MtmMean'] * df['taker_buy_mean']

    del df['MtmMean'], df['vma'], df['taker_buy_ma'], df['taker_buy_mean']

    return df
