from __future__ import annotations

import streamlit as st

from bettywhite_alpha.domain.models import DashboardSnapshot
from bettywhite_alpha.ui.components.cards import (
    render_metric_strip,
    render_news_panel,
    render_placeholder_panel,
    render_section_header,
    render_signal_cards,
)
from bettywhite_alpha.ui.components.charts import render_pnl_chart, render_price_chart
from bettywhite_alpha.ui.components.tables import render_positions_table, render_watchlist_table


def render_dashboard(snapshot: DashboardSnapshot) -> None:
    _render_hero(snapshot)
    render_metric_strip(snapshot.metrics)
    st.markdown("")

    chart_col, signal_col = st.columns([2.15, 1], gap="large")
    with chart_col:
        render_section_header(
            "Price Action",
            f"{snapshot.symbol} candlesticks with execution benchmarks layered over the active session.",
        )
        render_price_chart(snapshot.price_history, snapshot.symbol)

    with signal_col:
        render_section_header(
            "AI Signal Stack",
            "Model-like cards derived from VWAP, TWAP, mean reversion, and volatility state.",
        )
        render_signal_cards(snapshot.ai_signals)

    watchlist_col, positions_col, news_col = st.columns(3, gap="large")
    with watchlist_col:
        render_section_header("Watchlist", "High-priority instruments and desk bias.")
        render_watchlist_table(snapshot.watchlist)

    with positions_col:
        render_section_header("Positions", "Current exposure, average price, and open risk.")
        render_positions_table(snapshot.positions)

    with news_col:
        render_section_header("News Placeholder", "Reserved for live headlines, macro catalysts, and desk notes.")
        render_news_panel(snapshot.news)

    pnl_col, placeholder_col = st.columns([1.65, 1], gap="large")
    with pnl_col:
        render_section_header("PnL Curve", "Intraday equity drift with room for realized and open decomposition later.")
        render_pnl_chart(snapshot.pnl_curve)

    with placeholder_col:
        render_section_header("Auction Modules", "Slots reserved for profile and market-structure tooling.")
        for title, bullet_points in snapshot.placeholder_panels.items():
            render_placeholder_panel(title, bullet_points)


def _render_hero(snapshot: DashboardSnapshot) -> None:
    generated_at = snapshot.generated_at.strftime("%d %b %Y %H:%M")
    st.markdown(
        f"""
        <div class="bw-hero">
            <h1 class="bw-title">BettyWhite Alpha</h1>
            <p class="bw-subtitle">
                Institutional-style execution dashboard scaffold with a modular Python architecture.
                The current build runs on a mock feed, but the provider boundary is already in place for Sierra Chart,
                broker APIs, or custom market-data services.
            </p>
            <div class="bw-badge-row">
                <span class="bw-badge">Instrument: {snapshot.symbol}</span>
                <span class="bw-badge">Timeframe: {snapshot.timeframe}</span>
                <span class="bw-badge">Session Lens: {snapshot.session_mode}</span>
                <span class="bw-badge">Feed: {snapshot.provider_label}</span>
                <span class="bw-badge">Updated: {generated_at}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
