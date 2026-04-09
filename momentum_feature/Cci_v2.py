import talib as ta


eps = 1e-8


def signal(*args):
    # Cci_v2 indicator (WMA-based CCI using all four prices)
    # Formula: OMA=WMA(OPEN,N); HMA=WMA(HIGH,N); LMA=WMA(LOW,N); CMA=WMA(CLOSE,N)
    #          TP = (HMA + LMA + CMA + OMA) / 4; MA = WMA(TP, N)
    #          MD = MA(|MA - CMA|, N); result = (TP - MA) / (MD + eps)
    # Variant of CCI using WMA-smoothed OHLC prices as the typical price.
    # Positive values indicate the WMA typical price is above its mean deviation (bullish); negative below.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    oma = ta.WMA(df['open'], timeperiod=n)
    hma = ta.WMA(df['high'], timeperiod=n)
    lma = ta.WMA(df['low'], timeperiod=n)
    cma = ta.WMA(df['close'], timeperiod=n)

    tp = (hma + lma + cma + oma) / 4
    ma = ta.WMA(tp, n)
    md = abs(ma - cma).rolling(n, min_periods=1).mean()  # MD=MA(ABS(TP-MA),N)
    df[factor_name] = (tp - ma) / (md + eps)

    return df
