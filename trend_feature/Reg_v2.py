import talib as ta


eps = 1e-8


def signal(*args):
    # Reg_v2 indicator (Close vs longer-period linear regression, percentage)
    # Formula: REG = LINEARREG(CLOSE, 2N); result = 100 * (CLOSE - REG) / (REG + eps)
    # Measures the percentage deviation of close from its 2N-period linear regression value.
    # Uses a longer regression window (2N) than Reg.py for a smoother trend baseline.
    # Positive values indicate close is above the regression line; negative below.
    df = args[0]
    n = args[1]
    factor_name = args[2]
    
    df['LINEARREG'] = ta.LINEARREG(df['close'], timeperiod=2 * n)
    df[factor_name] = 100 * (df['close'] - df['LINEARREG']) / (df['LINEARREG'] + eps)

    # remove redundant columns
    del df['LINEARREG']

    return df
