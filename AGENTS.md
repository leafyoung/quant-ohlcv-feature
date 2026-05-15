# AGENTS.md — Coding Conventions for Indicator Development

This file documents the numerical and API patterns that must be followed when writing or modifying indicator files. All 335+ indicators live under `impl_pandas/` and `impl_polars/` and share a uniform `signal(df, n, factor_name, config)` signature.

## Config-Driven Numerical Defaults

All numerical parameters come from `IndicatorConfig` (defined in `indicator_config.py`). **Never hardcode numerical constants.**

```python
@dataclass(frozen=True)
class IndicatorConfig:
    min_periods: Optional[int] = None   # rolling window min_periods / min_samples
    ddof: int = 1                       # delta degrees of freedom for std
    ewm_adjust: bool = True             # ewm adjust parameter
    eps: float = 1e-8                   # division-by-zero floor
    normalize_eps: float = 1e-9         # normalization / comparison epsilon
```

### Which epsilon to use

| Constant | Field | When to use |
|---|---|---|
| Division-by-zero guard | `config.eps` (1e-8) | Denominators in `/ col`, `/ rolling_std()`, `/ rolling_sum()`, `/ range`, `/ computed_intermediate` |
| Comparison / threshold | `config.normalize_eps` (1e-9) | `np.where(np.abs(prev) > eps, ...)`, std-zero thresholds, boundary comparisons |

**Never use `config.normalize_eps` as a `+ eps` division guard.** It is 10× smaller than `config.eps` and intended only for `np.where` threshold comparisons. Using it as a denominator guard is inconsistent with the rest of the codebase.

```python
# ✗ WRONG — wrong epsilon for division guard
result = numerator / (config.normalize_eps + denominator)

# ✓ CORRECT — use config.eps for +eps pattern
result = numerator / (denominator + config.eps)
```

## Numerical Safety Rules

### 0. Use `config.eps` directly — never alias to bare `eps`

Do not create local aliases like `eps = config.eps`. Use `config.eps` directly at every use site.
This ensures grep-ability and prevents inconsistency when a file is partially migrated.

```python
# ✗ WRONG — local alias obscures the source of eps
    eps = config.eps
    df["result"] = numerator / (denominator + eps)

# ✓ CORRECT — use config.eps directly
    df["result"] = numerator / (denominator + config.eps)
```

### 1. Protect every computed denominator with `+ config.eps`

Any division by a column that is not raw OHLCV (i.e. a rolling stat, a shifted value, or an intermediate calculation) **must** add `config.eps` to the denominator.

```python
# ✗ WRONG — division by zero when std = 0 (flat price window)
df["grid"] = (df["close"] - df["median"]) / df["std"]

# ✓ CORRECT
df["grid"] = (df["close"] - df["median"]) / (df["std"] + config.eps)
```

This applies to all of these patterns:

| Denominator type | Example | Risk |
|---|---|---|
| Rolling std (including in helpers) | `df["close"].rolling(n).std()`, `scale_zscore()` | Zero when price is flat for N bars |
| Rolling sum of price range | `(df["high"] - df["open"]).rolling(n).sum()` | Zero when open==high for N bars |
| Rolling sum of abs diff | `df["abs_diff_close"].rolling(n).sum()` | Zero when price is unchanged for N bars |
| Rolling sum of volume/TR | `df["TR_sum"]`, `df["vma"]`, `df["volume"].rolling(n).sum()` | Zero for illiquid assets or first N bars |
| Shifted price/volume | `df["close"].shift(n)`, `df["volume"].shift(n)` | Zero if bar has zero close/volume |
| Rolling mean (as denominator) | `df["sma"]`, `df["ma"]`, `df["median"]` | Zero for delisted assets |
| Intermediate computed range | `df["max_high"] - df["min_low"]`, `max_price - min_price` | Zero when high==low for N bars |
| Intermediate computed ratio | `df["volume_ratio"]`, `df["R"]`, `df["span_B"]` | Zero from degenerate inputs |
| Normalized intermediate | `df["normalized_shortest_path"]`, `df["open"]` | Zero when high==low==open==close |
| Computed midpoint / cloud level | `df["span_B"]`, `df["span_A"]` | Zero from rolling extremes coincidence |

### 1a. Helper functions must also protect denominators

The shared helpers (`scale_zscore`, `scale_01`) are used by many indicators. Their internal rolling operations must also add `config.eps`:

```python
# helpers.py — scale_zscore
_s = (pd.Series(_s) - pd.Series(_s).rolling(_n).mean()) / (
    pd.Series(_s).rolling(_n).std(ddof=config.ddof) + config.eps
)
```

### 1b. Multi-level computations need eps at every division

When an indicator chains multiple divisions, each denominator needs its own guard:

```python
# PriceVolumeResist — two divisions, two guards
df["volume_ratio"] = (...) / (df["volume_shift"] + config.eps)
df[factor_name] = df["close_ratio"] / (df["volume_ratio"] + config.eps) * ...

# Amihud — intermediate column as denominator
df["normalized_shortest_path"] = df["intraday_shortest_path"] / df["open"]
df["liquidity_premium"] = df["quote_volume"] / (df["normalized_shortest_path"] + config.eps)

# Ic (Ichimoku Cloud) — span_B is a midpoint of rolling extremes
df[factor_name] = df["span_A"] / (df["span_B"] + config.eps)

# Vidya — rolling sum of abs differences can be zero in flat market
VI = df["abs_diff_close_n"] / (df["abs_diff_close_sum"] + config.eps)
```

### 2. Rolling range denominators must use both bounds

When computing price position within a rolling range, the denominator is `(max - min)`, not `(max - current)`.

```python
# ✗ WRONG — uses current low instead of rolling min
df["price_ch"] = 2 * (df["price"] - df["min_low"]) / (df["max_high"] - df["low"]) - 0.5

# ✓ CORRECT — full rolling range with eps guard
df["price_ch"] = 2 * (df["price"] - df["min_low"]) / (df["max_high"] - df["min_low"] + config.eps) - 0.5
```

### 3. Never use `pct_change()` — implement manual return with `config.eps`

`pct_change()` does not protect against division by zero when the shifted price is zero.
Always implement returns manually with `+ config.eps` on the shifted close:

```python
# ✗ WRONG — no division-by-zero protection
df["ret"] = df["close"].pct_change(n)
df["ret"] = df["close"].pct_change()

# ✓ CORRECT — manual with config.eps
df["ret"] = df["close"] / (df["close"].shift(n) + config.eps) - 1
df["ret"] = df["close"] / (df["close"].shift(1) + config.eps) - 1
```

When implementing custom pct_change with a denominator floor for comparison thresholds:

```python
# ✗ WRONG — hardcoded epsilon
df[factor_name] = (grid_arr - prev) / np.where(np.abs(prev) > 1e-9, prev, np.nan)

# ✓ CORRECT — config-driven
df[factor_name] = (grid_arr - prev) / np.where(np.abs(prev) > config.normalize_eps, prev, np.nan)
```

### 4. `+ config.eps` must be inside the denominator parentheses

Due to operator precedence, `+ config.eps` placed after the closing parenthesis of the
denominator adds to the **result** of the division, not the denominator itself — making
the guard a no-op.

```python
# ✗ WRONG — eps is outside the denominator; no division-by-zero protection
df["XRM"] = df["XR"].rolling(n).sum() / df["TR"].rolling(n).sum() + config.eps

# ✓ CORRECT — eps is inside the denominator
df["XRM"] = df["XR"].rolling(n).sum() / (df["TR"].rolling(n).sum() + config.eps)
```

When in doubt, wrap the entire denominator in an extra pair of parentheses.

### 5. Never use `inplace=True` on pandas operations

In-place mutations on DataFrame columns can corrupt the caller's data.

```python
# ✗ WRONG — mutates caller's Series
ser.fillna(value=0, inplace=True)
df["col"].fillna(value=0, inplace=True)

# ✓ CORRECT — returns new object
ser = ser.fillna(value=0)
df["col"] = df["col"].fillna(0)
```

Exception: `df.drop(columns=[...], inplace=True)` on local DataFrames is acceptable when the DataFrame is not shared with callers. However, the assignment form is preferred for clarity:

```python
# Preferred:
df = df.drop(columns=[...])       # pandas
df = df.drop(["col1", "col2"])    # polars
```

### 6. Use standard True Range (TR) with previous close

The True Range must use the **previous** bar's close (`close.shift(1)`), not the current
bar's close. This is the standard Wilder definition used in ATR, ADX, and related indicators.

```python
# ✗ WRONG — uses current close
df["c2"] = abs(df["high"] - df["close"])
df["c3"] = abs(df["low"] - df["close"])

# ✓ CORRECT — uses previous close (standard Wilder TR)
df["c1"] = df["high"] - df["low"]
df["c2"] = abs(df["high"] - df["close"].shift(1))
df["c3"] = abs(df["low"] - df["close"].shift(1))
df["TR"] = df[["c1", "c2", "c3"]].max(axis=1)
```

### 7. Use closed-form OLS instead of sklearn for rolling regression

Never import `sklearn.linear_model.LinearRegression` inside indicator files. It allocates an object per rolling window, triggers SVD, and can fail to converge on short windows.

```python
# ✗ WRONG — sklearn per row, SVD can fail
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(x.reshape(-1, 1), y)

# ✓ CORRECT — closed-form OLS, O(N) per window, no external deps
x = np.arange(m, dtype=float)
x_mean = (m - 1) / 2.0
y_mean = y_arr.mean()
slope = np.dot(x - x_mean, y_arr - y_mean) / (np.dot(x - x_mean, x - x_mean) + config.eps)
intercept = y_mean - slope * x_mean
return slope * (m - 1) + intercept
```

### 8. Use identical algorithms in both impls for cross-impl numerical match

When optimizing a computation (e.g. replacing a while loop), apply the **same algorithm** in both `impl_pandas/` and `impl_polars/`. Different algorithms (e.g. `rolling().rank()` in pandas vs numpy loop in polars) produce different numerics and defeat the cross-impl comparison test.

```python
# Both impls should use the same numpy loop:
pmar_np = df["pmar"].to_numpy()
result = np.full(len(pmar_np), np.nan)
for i in range(min_periods - 1, len(pmar_np)):
    window = pmar_np[max(0, i - n) : i + 1]
    result[i] = np.sum(window < pmar_np[i]) / n * 100
```

## Rolling Window Configuration

Always pass config parameters to rolling/EWM calls:

```python
# pandas
df["col"].rolling(n, min_periods=config.min_periods)
df["col"].std(ddof=config.ddof)
df["col"].ewm(span=n, adjust=config.ewm_adjust)

# polars
df["col"].rolling_min(n, min_samples=config.min_periods)
df["col"].rolling_std(n, min_samples=config.min_periods, ddof=config.ddof)
```

## Polars-Specific Rules

- Use `fill_nan(None)` to convert float NaN → polars null (so aggregations skip them, matching pandas behavior).
- Use `fill_null(0)` only when intentional (early zero-fill before division is dangerous — prefer `fill_nan(None)`).
- `np.where()` on polars Series produces NaN (not null); always chain `.fill_nan(None)`.

## RSI-style ratio patterns need eps

When computing an RSI or similar ratio of the form `a / (a + b)`, the denominator is a
computed sum that can be zero:

```python
# ✗ WRONG — (a + b) can be zero
df["rsi"] = a / (a + b) * 100

# ✓ CORRECT
df["rsi"] = a / (a + b + config.eps) * 100
```

This applies to any indicator that divides by a sum of positive/negative components:
RSI, Imi, Do, Demaker, Bbw, etc.

## Conditional division — prefer `+ config.eps` over `np.where` guards

When a denominator can be zero, prefer adding `+ config.eps` over using `np.where` to
conditionally avoid the division. The `+ config.eps` pattern is simpler, more consistent,
and avoids the need to decide what value to produce when the denominator is zero.

```python
# ✗ INCONSISTENT — np.where guard produces a different value at zero
df[factor_name] = np.where(df["path_shortest"] == 0, 0, df["quote_volume"] / df["path_shortest"])

# ✓ CORRECT — uniform + config.eps pattern
df[factor_name] = df["quote_volume"] / (df["path_shortest"] + config.eps)
```

## File Structure

Every indicator file must:
- Export a single `signal(df, n, factor_name, config)` function.
- Delete all intermediate columns before returning `df`.
- Have a docstring with the formula in pseudo-math notation.
- Have an identical counterpart in the other impl with the same algorithm.

## Testing

```bash
python tests/run_suite_parallel.py --impl pandas   # 187,600 test cases
python tests/run_suite_parallel.py --impl polars    # 187,600 test cases
python tests/compare.py <pandas.csv> <polars.csv>   # cross-impl comparison
```

Both impls must pass 187,600/187,600 with zero failures. Cross-impl numerical match target: ≥99.8%.

## Known Remaining Floating-Point Diffs

As of this update, 357/187,600 cases (0.19%) show small FP differences between pandas and polars in these indicators:
- `ZfAbsMean` (293 diffs, max_rel 1.4e-3) — recursive EMA accumulation
- `Stc` (17 diffs), `Acs` (10 diffs) — TA-Lib FP boundary
- `LongMoment`/`ShortMoment` (12 diffs) — higher-moment statistics
- `Grid` (3 diffs), `Qstick` (4 diffs) — inf from zero denominators in edge cases

These are acceptable FP-level differences and do not indicate logic errors.
