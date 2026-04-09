import pandas as pd


def signal(*args):
    # Vao indicator (Volume Analysis Oscillator)
    # Formula: WV = VOLUME * (CLOSE - 0.5*HIGH - 0.5*LOW); VAO = WV + REF(WV, 1)
    #          result = MA(VAO, N) - MA(VAO, 3N)
    # Weights volume by how far the close is from the midpoint of the candle (above midpoint = buying,
    # below = selling). The difference of short and long MAs acts as an oscillator around zero.
    # Positive values indicate net buying pressure; negative values indicate selling pressure.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    wv = df['volume'] * (df['close'] - 0.5 * df['high'] - 0.5 * df['low'])
    _vao = wv + wv.shift(1)
    vao_ma1 = _vao.rolling(n, min_periods=1).mean()
    vao_ma2 = _vao.rolling(int(3*n), min_periods=1).mean()

    df[factor_name] = pd.Series(vao_ma1 - vao_ma2)

    return df
