import talib as ta


eps = 1e-8


def signal(*args):
    # RegTema indicator (TEMA vs its linear regression)
    # Formula: EMA1 = EMA(CLOSE,N); EMA2 = EMA(EMA1,N); EMA3 = EMA(EMA2,N)
    #          TEMA = 3*EMA1 - 3*EMA2 + EMA3; REG_TEMA = LINEARREG(TEMA,N)
    #          result = TEMA / (REG_TEMA + eps) - 1
    # Measures how far the triple exponential MA has deviated from its own linear trend.
    # Positive values indicate TEMA is above its regression line (upward momentum); negative below.
    df = args[0]
    n = args[1]
    factor_name = args[2]
    
    ema = df['close'].ewm(span=n, adjust=False).mean()
    emax2 = ema.ewm(span=n, adjust=False).mean()
    emax3 = emax2.ewm(span=n, adjust=False).mean()
    tema = 3 * ema - 3 * emax2 + emax3

    # calculate regression
    reg_tema = ta.LINEARREG(tema, timeperiod=n)  # talib built-in linear regression
    df[factor_name] = tema / (reg_tema + eps) - 1

    return df
