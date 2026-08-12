from __future__ import annotations

import numpy as np
import pandas as pd


def add_execution_benchmarks(frame: pd.DataFrame) -> pd.DataFrame:
    enriched = frame.copy()
    typical_price = (enriched["high"] + enriched["low"] + enriched["close"]) / 3
    cumulative_volume = enriched["volume"].replace(0, np.nan).cumsum()
    enriched["vwap"] = (typical_price * enriched["volume"]).cumsum() / cumulative_volume
    enriched["twap"] = typical_price.expanding().mean()
    enriched["return_pct"] = enriched["close"].pct_change().fillna(0.0)
    enriched["rolling_volatility"] = enriched["return_pct"].rolling(20).std().fillna(0.0)
    return enriched


def calculate_max_drawdown(curve: pd.Series) -> float:
    running_peak = curve.cummax()
    drawdown = curve - running_peak
    return float(drawdown.min())

