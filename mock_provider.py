from __future__ import annotations

from datetime import datetime
from hashlib import sha256

import numpy as np
import pandas as pd

from bettywhite_alpha.config import SYMBOL_BASE_PRICES, SYMBOL_OPTIONS, TIMEFRAME_TO_FREQ
from bettywhite_alpha.data.providers import MarketDataProvider
from bettywhite_alpha.domain.models import NewsItem


class MockMarketDataProvider(MarketDataProvider):
    label = "Mock Feed"

    def get_price_history(self, symbol: str, timeframe: str, bars: int) -> pd.DataFrame:
        rng = np.random.default_rng(self._seed(symbol, timeframe))
        freq = TIMEFRAME_TO_FREQ[timeframe]
        end = pd.Timestamp(datetime.now()).floor("min")
        index = pd.date_range(end=end, periods=bars, freq=freq)

        base_price = SYMBOL_BASE_PRICES.get(symbol, 100.0)
        drift = rng.normal(loc=0.02, scale=0.16, size=bars).cumsum()
        cycle = np.sin(np.linspace(0, 5 * np.pi, bars)) * max(base_price * 0.0009, 0.35)
        close = base_price + drift + cycle
        open_ = np.roll(close, 1)
        open_[0] = close[0] - rng.normal(0, max(base_price * 0.0004, 0.18))
        open_ = open_ + rng.normal(0, max(base_price * 0.00015, 0.08), size=bars)
        high = np.maximum(open_, close) + rng.uniform(max(base_price * 0.0001, 0.06), max(base_price * 0.0007, 0.48), size=bars)
        low = np.minimum(open_, close) - rng.uniform(max(base_price * 0.0001, 0.06), max(base_price * 0.0007, 0.48), size=bars)
        volume = (rng.integers(280, 1600, size=bars) * (1 + np.abs(np.gradient(close)))).astype(int)

        return pd.DataFrame(
            {
                "timestamp": index,
                "open": open_,
                "high": high,
                "low": low,
                "close": close,
                "volume": volume,
            }
        )

    def get_watchlist(self, primary_symbol: str) -> pd.DataFrame:
        symbols = [primary_symbol, *[symbol for symbol in SYMBOL_OPTIONS if symbol != primary_symbol][:5]]
        rows: list[dict[str, object]] = []

        for idx, symbol in enumerate(symbols):
            rng = np.random.default_rng(self._seed(symbol, f"watchlist-{idx}"))
            last_price = SYMBOL_BASE_PRICES.get(symbol, 100.0) + rng.normal(0, 2.4)
            change_pct = rng.normal(0.15, 0.9)
            volume = int(rng.integers(18_000, 125_000))
            signal = np.random.default_rng(self._seed(symbol, "signal")).choice(["Long Bias", "Neutral", "Fade Setup"])
            rows.append(
                {
                    "symbol": symbol,
                    "last": last_price,
                    "change_pct": change_pct,
                    "volume": volume,
                    "signal": signal,
                }
            )

        return pd.DataFrame(rows)

    def get_positions(self, primary_symbol: str) -> pd.DataFrame:
        fallback_symbols = [symbol for symbol in ("NQ", "CL", "GC", "RTY") if symbol != primary_symbol]
        seeds = [
            (primary_symbol, "Long", 4),
            (fallback_symbols[0], "Short", 2),
            (fallback_symbols[1], "Long", 3),
        ]
        rows: list[dict[str, object]] = []

        for symbol, side, qty in seeds:
            rng = np.random.default_rng(self._seed(symbol, "position"))
            avg_price = SYMBOL_BASE_PRICES.get(symbol, 100.0) + rng.normal(0, 1.4)
            last_price = avg_price + rng.normal(0, 4.2)
            multiplier = 1 if side == "Long" else -1
            open_pnl = (last_price - avg_price) * qty * multiplier * 12
            risk = rng.choice(["Core", "Probe", "Hedge"])
            rows.append(
                {
                    "symbol": symbol,
                    "side": side,
                    "qty": qty,
                    "avg_price": avg_price,
                    "last_price": last_price,
                    "open_pnl": open_pnl,
                    "risk_bucket": risk,
                }
            )

        return pd.DataFrame(rows)

    def get_pnl_curve(self, primary_symbol: str, bars: int) -> pd.DataFrame:
        rng = np.random.default_rng(self._seed(primary_symbol, "pnl"))
        periods = max(60, min(bars, 240))
        index = pd.date_range(end=pd.Timestamp(datetime.now()).floor("min"), periods=periods, freq="3min")
        increments = rng.normal(loc=42, scale=165, size=periods)
        curve = increments.cumsum() - increments[0]
        return pd.DataFrame({"timestamp": index, "pnl": curve})

    def get_news(self, primary_symbol: str) -> list[NewsItem]:
        return [
            NewsItem(
                headline=f"{primary_symbol} session flow placeholder awaits live headline bridge",
                source="Desk Notes",
                timestamp="Now",
                sentiment="Neutral",
            ),
            NewsItem(
                headline="Macro event wiring point reserved for economic calendar and breaking news feeds",
                source="Macro Feed",
                timestamp="08:30",
                sentiment="Watch",
            ),
            NewsItem(
                headline="Order-flow commentary card can be linked to Sierra, Rithmic, or custom inference services",
                source="Alpha Ops",
                timestamp="07:55",
                sentiment="Build",
            ),
        ]

    @staticmethod
    def _seed(symbol: str, suffix: str) -> int:
        token = f"{symbol}-{suffix}".encode("utf-8")
        return int(sha256(token).hexdigest()[:8], 16)
