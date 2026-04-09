import numpy as np


def signal(*args):
    # ShortMoment indicator (Momentum based on low-amplitude candles, short window)
    # Formula: PRICE_CHANGE = CLOSE.pct_change(N); AMPLITUDE = HIGH/LOW - 1
    #          Within an N rolling window, select the 70% lowest-amplitude candles,
    #          result = SUM of their PRICE_CHANGEs
    # A shorter-window version of LongMoment. Captures momentum from calm, low-volatility candles
    # within a tighter N-period window for quicker signal response.
    df = args[0]
    n = args[1]
    factor_name = args[2]

    def range_plus(x, np_tmp, rolling_window, lam):
        # calculate the rolling index
        li = x.index.to_list()
        # extract the corresponding index block from the full array
        np_tmp2 = np_tmp[li, :]
        # sort by amplitude
        np_tmp2 = np_tmp2[np.argsort(np_tmp2[:, 0])]
        # calculate the number of splits needed
        t = int(rolling_window * lam)
        # calculate low-price return factor
        np_tmp2 = np_tmp2[:t, :]
        s = np_tmp2[:, 1].sum()
        return s

    df['price_change'] = df['close'].pct_change(n)
    # calculate cut momentum and reversal factor for window 20-180
    df['amplitude'] = (df['high'] / df['low']) - 1
    # convert the two rolling columns to array first
    np_tmp = df[['amplitude', 'price_change']].values
    # calculate the factor
    df[factor_name] = df['price_change'].rolling(n).apply(
        range_plus, args=(np_tmp, n, 0.7), raw=False)

    del df['amplitude'], df['price_change']

    return df
