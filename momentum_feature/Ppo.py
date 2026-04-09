def signal(*args):
    # Ppo indicator (Percentage Price Oscillator with EMA signal line)
    # Formula: N1 = N*1.382; N2 = 3N; N3 = N
    #          PPO = (EMA(CLOSE,N1) - EMA(CLOSE,N2)) / EMA(CLOSE,N2)
    #          result = EMA(PPO, N3)  (signal line)
    # PPO measures the percentage difference between a shorter and longer EMA, similar to MACD but normalized.
    # The EMA signal line smooths the PPO for trading signal generation.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    N3 = n
    N1 = int(n * 1.382)
    N2 = 3 * n
    df['ema_1'] = df['close'].ewm(
        N1, adjust=False).mean()  # EMA(CLOSE,N1)
    df['ema_2'] = df['close'].ewm(
        N2, adjust=False).mean()  # EMA(CLOSE,N2)
    # PPO=(EMA(CLOSE,N1)-EMA(CLOSE,N2))/EMA(CLOSE,N2)
    df['PPO'] = (df['ema_1'] - df['ema_2']) / df['ema_2']
    df[factor_name] = df['PPO'].ewm(N3, adjust=False).mean()  # PPO_SIGNAL=EMA(PPO,N3)

    del df['ema_1']
    del df['ema_2']
    del df['PPO']

    return df
