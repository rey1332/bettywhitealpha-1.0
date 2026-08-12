from __future__ import annotations

from datetime import datetime

import numpy as np
import pandas as pd

from bettywhite_alpha.analytics.indicators import add_execution_benchmarks, calculate_max_drawdown
from bettywhite_alpha.data.providers import MarketDataProvider
from bettywhite_alpha.domain.models import DashboardSnapshot, PerformanceMetrics, SignalCard


class DashboardService:
    def __init__(self, provider: MarketDataProvider) -> None:
        self.provider = provider

    def load_snapshot(
        self,
        symbol: str,
        timeframe: str,
        bars: int,
        session_mode: str,
    ) -> DashboardSnapshot:
        price_history = add_execution_benchmarks(self.provider.get_price_history(symbol, timeframe, bars))
        watchlist = self.provider.get_watchlist(symbol)
        positions = self.provider.get_positions(symbol)
        pnl_curve = self.provider.get_pnl_curve(symbol, bars)
        news = self.provider.get_news(symbol)

        return DashboardSnapshot(
            symbol=symbol,
            timeframe=timeframe,
            session_mode=session_mode,
            generated_at=datetime.now(),
            provider_label=self.provider.label,
            price_history=price_history,
            watchlist=watchlist,
            positions=positions,
            pnl_curve=pnl_curve,
            metrics=self._build_metrics(price_history, positions, pnl_curve),
            ai_signals=self._build_ai_signals(price_history, session_mode),
            news=news,
            placeholder_panels=self._build_placeholders(),
        )

    @staticmethod
    def _build_metrics(
        price_history: pd.DataFrame,
        positions: pd.DataFrame,
        pnl_curve: pd.DataFrame,
    ) -> PerformanceMetrics:
        daily_pnl = float(pnl_curve["pnl"].iloc[-1])
        open_pnl = float(positions["open_pnl"].sum())
        realized_pnl = daily_pnl - open_pnl
        session_return = float((price_history["close"].iloc[-1] / price_history["open"].iloc[0]) - 1.0)
        max_drawdown = calculate_max_drawdown(pnl_curve["pnl"])

        side_multiplier = positions["side"].map({"Long": 1, "Short": -1}).fillna(0)
        net_exposure = float((positions["last_price"] * positions["qty"] * side_multiplier).sum())

        return PerformanceMetrics(
            daily_pnl=daily_pnl,
            open_pnl=open_pnl,
            realized_pnl=realized_pnl,
            session_return=session_return,
            max_drawdown=max_drawdown,
            net_exposure=net_exposure,
        )

    @staticmethod
    def _build_ai_signals(price_history: pd.DataFrame, session_mode: str) -> list[SignalCard]:
        close = float(price_history["close"].iloc[-1])
        vwap = float(price_history["vwap"].iloc[-1])
        twap = float(price_history["twap"].iloc[-1])
        recent_returns = price_history["return_pct"].tail(24)
        volatility = float(recent_returns.std() * np.sqrt(len(recent_returns)) * 100)
        vwap_gap_pct = ((close - vwap) / vwap) * 100 if vwap else 0.0
        twap_gap_pct = ((close - twap) / twap) * 100 if twap else 0.0
        z_score = DashboardService._z_score(price_history["close"].tail(20))

        trend_direction = "Long" if close >= twap else "Short"
        trend_confidence = min(96, 54 + int(abs(twap_gap_pct) * 26))

        execution_direction = "Aligned" if abs(vwap_gap_pct) < 0.18 else "Extended"
        execution_confidence = min(98, 58 + int(max(abs(vwap_gap_pct), 0.02) * 80))

        mean_reversion_direction = "Fade" if abs(z_score) >= 1.2 else "Hold"
        mean_reversion_confidence = min(95, 52 + int(abs(z_score) * 18))

        risk_regime = "Compression" if volatility < 0.8 else "Expansion"
        risk_confidence = min(93, 57 + int(volatility * 12))

        return [
            SignalCard(
                title="Trend Pulse",
                direction=trend_direction,
                confidence=trend_confidence,
                regime=session_mode,
                summary=f"Price is {twap_gap_pct:+.2f}% versus TWAP, keeping directional pressure biased {trend_direction.lower()}.",
            ),
            SignalCard(
                title="Execution Quality",
                direction=execution_direction,
                confidence=execution_confidence,
                regime="VWAP",
                summary=f"Last trade sits {vwap_gap_pct:+.2f}% from VWAP, useful for pacing entries and scale-outs.",
            ),
            SignalCard(
                title="Mean Reversion",
                direction=mean_reversion_direction,
                confidence=mean_reversion_confidence,
                regime="20-bar",
                summary=f"Close location z-score is {z_score:+.2f}; fade logic arms only when extension pushes beyond the balance zone.",
            ),
            SignalCard(
                title="Risk Regime",
                direction=risk_regime,
                confidence=risk_confidence,
                regime="Volatility",
                summary=f"Recent realized volatility is {volatility:.2f}; size and stop logic should adapt to this regime.",
            ),
        ]

    @staticmethod
    def _build_placeholders() -> dict[str, list[str]]:
        return {
            "Volume Profile": [
                "Reserve this panel for session volume-at-price histograms.",
                "Add composite profiles, HVN/LVN tagging, and POC shift tracking.",
            ],
            "TPO / Auction Map": [
                "Swap in letter-based distributions or custom auction visualizations.",
                "This slot is sized for bracket counts, IB ranges, and value migration.",
            ],
        }

    @staticmethod
    def _z_score(series: pd.Series) -> float:
        if len(series) < 2 or series.std() == 0:
            return 0.0
        return float((series.iloc[-1] - series.mean()) / series.std())
