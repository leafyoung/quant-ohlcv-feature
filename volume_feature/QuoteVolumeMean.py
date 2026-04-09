"""
Strategy Sharing Session
Position Management Framework

Copyright reserved.

This code is for personal learning use only. Copying, modification, or commercial use without authorization is prohibited.
"""
import os
import numpy as np
import pandas as pd


def signal(*args):
    df = args[0]
    n = args[1]
    factor_name = args[2]

    df[factor_name] = df['quote_volume'].rolling(n, min_periods=1).mean()

    return df


def signal_multi_params(df, param_list) -> dict:
    """
    Uses multi-parameter aggregated calculation for the same factor, which can effectively improve the speed
    of backtesting and live cal_factor, approximately 3x faster than `signal`.
    :param df: dataframe of k-line data
    :param param_list: parameter list
    """
    ret = dict()
    for param in param_list:
        n = int(param)
        ret[str(param)] = df['quote_volume'].rolling(n, min_periods=1).mean()
    return ret
