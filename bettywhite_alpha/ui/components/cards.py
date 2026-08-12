from __future__ import annotations

import streamlit as st

from bettywhite_alpha.domain.models import NewsItem, PerformanceMetrics, SignalCard


def render_section_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div>
            <p class="bw-section-title">{title}</p>
            <p class="bw-section-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_strip(metrics: PerformanceMetrics) -> None:
    cols = st.columns(6)
    cols[0].metric("Daily PnL", _format_currency(metrics.daily_pnl))
    cols[1].metric("Open PnL", _format_currency(metrics.open_pnl))
    cols[2].metric("Realized PnL", _format_currency(metrics.realized_pnl))
    cols[3].metric("Session Return", _format_percent(metrics.session_return))
    cols[4].metric("Max Drawdown", _format_currency(metrics.max_drawdown))
    cols[5].metric("Net Exposure", _format_currency(metrics.net_exposure))


def render_signal_cards(signals: list[SignalCard]) -> None:
    for signal in signals:
        pill_class = signal.direction.lower().replace(" ", "-")
        st.markdown(
            f"""
            <div class="bw-signal-card">
                <div class="bw-card-row">
                    <span class="bw-card-kicker">{signal.title}</span>
                    <span class="bw-pill {pill_class}">{signal.direction}</span>
                </div>
                <p class="bw-card-title">{signal.confidence}% confidence</p>
                <p class="bw-card-copy">{signal.summary}</p>
                <div class="bw-card-foot">Regime: {signal.regime}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_news_panel(news: list[NewsItem]) -> None:
    for item in news:
        st.markdown(
            f"""
            <div class="bw-news-card">
                <div class="bw-card-row">
                    <span class="bw-card-kicker">{item.source}</span>
                    <span class="bw-pill hold">{item.sentiment}</span>
                </div>
                <p class="bw-card-title">{item.headline}</p>
                <div class="bw-card-foot">{item.timestamp}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_placeholder_panel(title: str, bullet_points: list[str]) -> None:
    items = "".join(f"<li>{point}</li>" for point in bullet_points)
    st.markdown(
        f"""
        <div class="bw-placeholder-card">
            <span class="bw-card-kicker">Placeholder</span>
            <p class="bw-card-title">{title}</p>
            <ul class="bw-placeholder-list">{items}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _format_currency(value: float) -> str:
    return f"${value:,.0f}"


def _format_percent(value: float) -> str:
    return f"{value * 100:+.2f}%"

