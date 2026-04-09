import talib as ta


def signal(*args):
    # Acs indicator (Rolling std of ADX/close ratio)
    # Formula: ADX_CLOSE = ADX(N) / CLOSE; result = STD(ADX_CLOSE, N)
    # ADX measures trend strength; dividing by close normalizes for price level.
    # The rolling std captures how consistently ADX/close has been varying (volatility of trend strength).
    df = args[0]
    n  = args[1]
    factor_name = args[2]

    df['adx'] = ta.ADX(df['high'], df['low'], df['close'], n)
    df['adx_close'] = df['adx'] / df['close']
    df[factor_name] = df['adx_close'].rolling(n).std()

    del df['adx'], df['adx_close']

    return df
