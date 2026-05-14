import numpy as np
import polars as pl
from sklearn.linear_model import LinearRegression


def signal(df, n, factor_name, config):
    # Reg_v3 indicator (Close vs OLS linear regression using sklearn)
    # Formula: OLS fit of CLOSE over N time steps; REG = predicted value at last step (y = ax + b)
    #          result = CLOSE / (REG + eps) - 1
    # Uses sklearn LinearRegression to compute an N-period rolling OLS fit,
    # taking the fitted value at the last point as the regression baseline.
    # Positive values indicate close is above the fitted trend; negative below.
    eps = config.eps

    # sklearn linear regression
    def reg_ols(_y):
        _x = np.arange(n) + 1
        model = LinearRegression().fit(_x.reshape(-1, 1), _y)  # linear regression training
        y_pred = model.coef_ * _x + model.intercept_  # y = ax + b
        return y_pred[-1]

    # rolling OLS regression using numpy
    close_np = np.array(df["close"], dtype=float)
    reg_close = np.full(len(close_np), np.nan)
    min_periods = config.min_periods or 1
    for i in range(min_periods - 1, len(close_np)):
        start = max(0, i - n + 1)
        _y = close_np[start : i + 1]
        m = len(_y)
        _x = np.arange(m).reshape(-1, 1).astype(float)
        model = LinearRegression().fit(_x, _y)
        reg_close[i] = model.predict(_x[-1:])[0]
    df = df.with_columns(pl.Series("reg_close", reg_close))
    df = df.with_columns(pl.Series(factor_name, (df["close"] / (df["reg_close"] + eps) - 1).fill_nan(None)))

    # remove redundant columns
    df = df.drop("reg_close")

    return df
