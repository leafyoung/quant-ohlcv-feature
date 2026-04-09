def signal(*args):
    '''
    BiasCubic indicator - product of three bias values
    Minimize variables: back_hour_list = [3, 4, 6, 8, 9, 12, 24, 30, 36, 48, 60, 72, 96]
    Taking int(n / 2), dividing by 1.5, and multiplying by 1.5 to create three distinctions is also viable - achieving three uses from one variable.
    :param args:
    :return:
    '''
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df['ma_1'] = df['close'].rolling(int(n / 2), min_periods=1).mean()
    df['ma_2'] = df['close'].rolling(n, min_periods=1).mean()
    df['ma_3'] = df['close'].rolling(n * 2, min_periods=1).mean()
    df['bias_1'] = (df['close'] / df['ma_1'] - 1)
    df['bias_2'] = (df['close'] / df['ma_2'] - 1)
    df['bias_3'] = (df['close'] / df['ma_3'] - 1)

    df['mtm'] = (df['bias_1'] * df['bias_2'] *df['bias_3'])* df['quote_volume']/df['quote_volume'].rolling(n, min_periods=1).mean()
    df[factor_name] = df['mtm'].rolling(n, min_periods=1).mean()

    del df['ma_1'], df['ma_2'], df['ma_3'], df['bias_1'], df['bias_2'], df['bias_3'],df['mtm']

    return df
