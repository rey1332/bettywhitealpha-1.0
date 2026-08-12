from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import pandas as pd


@dataclass(slots=True)
class NewsItem:
    headline: str
    source: str
    timestamp: str
    sentiment: str


@dataclass(slots=True)
class SignalCard:
    title: str
    direction: str
    confidence: int
    regime: str
    summary: str


@dataclass(slots=True)
class PerformanceMetrics:
    daily_pnl: float
    open_pnl: float
    realized_pnl: float
    session_return: float
    max_drawdown: float
    net_exposure: float


@dataclass(slots=True)
class DashboardSnapshot:
    symbol: str
    timeframe: str
    session_mode: str
    generated_at: datetime
    provider_label: str
    price_history: pd.DataFrame
    watchlist: pd.DataFrame
    positions: pd.DataFrame
    pnl_curve: pd.DataFrame
    metrics: PerformanceMetrics
    ai_signals: list[SignalCard]
    news: list[NewsItem]
    placeholder_panels: dict[str, list[str]]

