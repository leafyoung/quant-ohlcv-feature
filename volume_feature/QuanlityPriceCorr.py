def signal(*args):
    # QuanlityPriceCorr indicator (Close-QuoteVolume Rolling Correlation)
    # Formula: result = CORR(CLOSE, QUOTE_VOLUME, N)
    # Measures the rolling Pearson correlation between close price and quote volume over N periods.
    # Positive correlation indicates volume tends to rise with price (bullish confirmation);
    # negative correlation indicates volume rises when price falls (distribution or panic selling).
    df = args[0]
    n = args[1]
    factor_name = args[2]
    
    df[factor_name] = df['close'].rolling(n).corr(df['quote_volume'])

    return df
