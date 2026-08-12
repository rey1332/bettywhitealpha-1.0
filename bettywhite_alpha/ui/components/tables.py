from __future__ import annotations

import streamlit as st


def render_watchlist_table(watchlist) -> None:
    display = watchlist.rename(
        columns={
            "symbol": "Symbol",
            "last": "Last",
            "change_pct": "Change %",
            "volume": "Volume",
            "signal": "Signal",
        }
    ).copy()
    display["Last"] = display["Last"].map(lambda value: f"{value:,.2f}")
    display["Change %"] = display["Change %"].map(lambda value: f"{value:+.2f}%")
    display["Volume"] = display["Volume"].map(lambda value: f"{value:,.0f}")

    st.dataframe(display, hide_index=True, use_container_width=True, height=292)


def render_positions_table(positions) -> None:
    display = positions.rename(
        columns={
            "symbol": "Symbol",
            "side": "Side",
            "qty": "Qty",
            "avg_price": "Avg",
            "last_price": "Last",
            "open_pnl": "Open PnL",
            "risk_bucket": "Risk",
        }
    ).copy()
    display["Avg"] = display["Avg"].map(lambda value: f"{value:,.2f}")
    display["Last"] = display["Last"].map(lambda value: f"{value:,.2f}")
    display["Open PnL"] = display["Open PnL"].map(lambda value: f"${value:,.0f}")

    st.dataframe(display, hide_index=True, use_container_width=True, height=292)

