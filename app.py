from __future__ import annotations

import streamlit as st

from bettywhite_alpha.config import (
    APP_ICON,
    APP_TITLE,
    DEFAULT_BARS,
    DEFAULT_SYMBOL,
    SESSION_MODES,
    SYMBOL_OPTIONS,
    TIMEFRAME_OPTIONS,
)
from bettywhite_alpha.data.mock_provider import MockMarketDataProvider
from bettywhite_alpha.services.dashboard_service import DashboardService
from bettywhite_alpha.ui.dashboard import render_dashboard
from bettywhite_alpha.ui.theme import apply_theme


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_theme()

    st.sidebar.markdown("## Desk Controls")
    symbol = st.sidebar.selectbox(
        "Primary Instrument",
        SYMBOL_OPTIONS,
        index=SYMBOL_OPTIONS.index(DEFAULT_SYMBOL),
    )
    timeframe = st.sidebar.selectbox("Timeframe", TIMEFRAME_OPTIONS, index=1)
    bars = st.sidebar.slider("Visible Bars", min_value=120, max_value=720, value=DEFAULT_BARS, step=60)
    session_mode = st.sidebar.radio("Session Lens", SESSION_MODES, index=0)

    st.sidebar.markdown("## Feed Status")
    st.sidebar.success("Mock feed online")
    st.sidebar.caption(
        "The UI already uses a provider interface, so the mock feed can be replaced with Sierra Chart or another data source later."
    )

    st.sidebar.markdown("## Roadmap")
    st.sidebar.markdown(
        "- Sierra Chart adapter\n"
        "- Volume-at-price ingestion\n"
        "- Real positions and risk\n"
        "- News and AI inference hooks"
    )

    service = DashboardService(provider=MockMarketDataProvider())
    snapshot = service.load_snapshot(
        symbol=symbol,
        timeframe=timeframe,
        bars=bars,
        session_mode=session_mode,
    )
    render_dashboard(snapshot)


if __name__ == "__main__":
    main()

