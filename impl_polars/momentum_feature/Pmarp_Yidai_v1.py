import numpy as np
import polars as pl


# Factor indicator name version: Pmarp_Yidai_v1
def signal(df, n, factor_name, config):
    # Pmarp_Yidai_v1 indicator (Percentile rank of close vs MA ratio)
    # Formula: PMAR = |CLOSE / MA(CLOSE, N)|
    #          result = (number of past N candles with PMAR < current PMAR) / N * 100
    # Computes the rolling percentile rank of the absolute close-to-MA ratio over N periods.
    # High values indicate current price deviation from MA is unusually large (potential reversal point).

    # calculate sma
    df = df.with_columns(pl.Series("sma", df["close"].rolling_mean(n, min_samples=config.min_periods)))

    # compare current price to sma (percentage): relative price change vs moving average
    df = df.with_columns(pl.Series("pmar", abs(df["close"] / df["sma"])))

    # calculate how many candles in the statistical range the current candle's feature value exceeds? returns percentage
    # count how many candles' pmar the current candle's pmar exceeds within the statistical period
    df = df.with_columns(pl.lit(0).alias("pmarpSum"))

    k = n
    while k > 0:
        df = df.with_columns(pl.Series("pmardiff", df["pmar"] - df["pmar"].shift(k)))
        df = df.with_columns(pl.Series("add", np.where(df["pmardiff"] > 0, 1, 0)).fill_nan(None))
        df = df.with_columns(pl.Series("pmarpSum", df["pmarpSum"] + df["add"]))
        k -= 1

    df = df.with_columns(pl.Series(factor_name, df["pmarpSum"] / n * 100))

    # remove redundant columns
    df = df.drop(["sma", "pmar", "pmardiff", "add", "pmarpSum"])

    return df
