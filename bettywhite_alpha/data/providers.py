from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from bettywhite_alpha.domain.models import NewsItem


class MarketDataProvider(ABC):
    label = "Unknown Provider"

    @abstractmethod
    def get_price_history(self, symbol: str, timeframe: str, bars: int) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_watchlist(self, primary_symbol: str) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_positions(self, primary_symbol: str) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_pnl_curve(self, primary_symbol: str, bars: int) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_news(self, primary_symbol: str) -> list[NewsItem]:
        raise NotImplementedError

