def signal(*args):
    # MtmBull indicator (MTM mean × ATR × Taker buy composite)
    # Formula: MTM_MEAN = MA(CLOSE/REF(MA,N)-1, N) * 100; ATR = MA(TR,N)/MA * 100
    #          TAKER_BUY_MEAN = MA(taker_buy/MA(quote_volume)*100, N)
    #          result = MTM_MEAN * ATR * TAKER_BUY_MEAN
    # Bullish composite: momentum × volatility × buyer-initiated volume.
    # Large positive values indicate strong upside momentum in a volatile, buyer-dominated market.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    # momentum
    df['ma'] = df['close'].rolling(window=n).mean()
    df['mtm'] = (df['close'] / df['ma'].shift(n) - 1) * 100
    df['mtm_mean'] = df['mtm'].rolling(window=n).mean()

    # average amplitude
    df['tr1'] = df['high'] - df['low']
    df['tr2'] = abs(df['high'] - df['close'].shift(1))
    df['tr3'] = abs(df['low'] - df['close'].shift(1))
    df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
    df['ATR_abs'] = df['tr'].rolling(window=n, min_periods=1).mean()
    df['ATR'] = df['ATR_abs'] / df['ma'] * 100

    # average taker buy volume
    df['vma'] = df['quote_volume'].rolling(n, min_periods=1).mean()
    df['taker_buy_ma'] = (df['taker_buy_quote_asset_volume'] / df['vma']) * 100
    df['taker_buy_mean'] = df['taker_buy_ma'].rolling(window=n).mean()

    # combined indicator
    df[factor_name] = df['mtm_mean'] * df['ATR'] * df['taker_buy_mean']

    drop_col = [
        'ma', 'mtm', 'mtm_mean', 'tr1', 'tr2', 'tr3', 'tr', 'ATR_abs', 'ATR',
        'vma', 'taker_buy_ma', 'taker_buy_mean',
    ]
    df.drop(columns=drop_col, inplace=True)

    return df
