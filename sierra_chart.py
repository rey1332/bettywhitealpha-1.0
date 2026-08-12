from __future__ import annotations

import pandas as pd

from bettywhite_alpha.data.providers import MarketDataProvider
from bettywhite_alpha.domain.models import NewsItem


class SierraChartProvider(MarketDataProvider):
    label = "Sierra Chart"

    def get_price_history(self, symbol: str, timeframe: str, bars: int) -> pd.DataFrame:
        raise NotImplementedError("Implement the Sierra Chart bridge for OHLCV ingestion.")

    def get_watchlist(self, primary_symbol: str) -> pd.DataFrame:
        raise NotImplementedError("Implement Sierra or broker watchlist ingestion.")

    def get_positions(self, primary_symbol: str) -> pd.DataFrame:
        raise NotImplementedError("Implement broker position and risk syncing.")

    def get_pnl_curve(self, primary_symbol: str, bars: int) -> pd.DataFrame:
        raise NotImplementedError("Implement realized and open PnL history retrieval.")

    def get_news(self, primary_symbol: str) -> list[NewsItem]:
        raise NotImplementedError("Attach a news or calendar service for live headlines.")
