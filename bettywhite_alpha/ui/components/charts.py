from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


def render_price_chart(price_history, symbol: str) -> None:
    figure = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.76, 0.24],
        vertical_spacing=0.04,
    )

    figure.add_trace(
        go.Candlestick(
            x=price_history["timestamp"],
            open=price_history["open"],
            high=price_history["high"],
            low=price_history["low"],
            close=price_history["close"],
            name=symbol,
            increasing_line_color="#4FD1C5",
            decreasing_line_color="#FF6B6B",
            increasing_fillcolor="#4FD1C5",
            decreasing_fillcolor="#FF6B6B",
        ),
        row=1,
        col=1,
    )

    figure.add_trace(
        go.Scatter(
            x=price_history["timestamp"],
            y=price_history["vwap"],
            name="VWAP",
            mode="lines",
            line={"color": "#F7B955", "width": 2.1},
        ),
        row=1,
        col=1,
    )

    figure.add_trace(
        go.Scatter(
            x=price_history["timestamp"],
            y=price_history["twap"],
            name="TWAP",
            mode="lines",
            line={"color": "#7DA6FF", "width": 1.7, "dash": "dot"},
        ),
        row=1,
        col=1,
    )

    volume_colors = ["#4FD1C5" if close >= open_ else "#FF6B6B" for open_, close in zip(price_history["open"], price_history["close"])]
    figure.add_trace(
        go.Bar(
            x=price_history["timestamp"],
            y=price_history["volume"],
            name="Volume",
            marker={"color": volume_colors, "opacity": 0.75},
        ),
        row=2,
        col=1,
    )

    figure.update_layout(
        margin={"l": 10, "r": 10, "t": 10, "b": 10},
        height=540,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
        },
        hovermode="x unified",
        xaxis_rangeslider_visible=False,
    )
    figure.update_xaxes(showgrid=False, zeroline=False)
    figure.update_yaxes(gridcolor="rgba(140,163,191,0.12)", zeroline=False)

    st.plotly_chart(
        figure,
        use_container_width=True,
        config={"displayModeBar": False, "displaylogo": False},
    )


def render_pnl_chart(pnl_curve) -> None:
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=pnl_curve["timestamp"],
            y=pnl_curve["pnl"],
            mode="lines",
            line={"color": "#4FD1C5", "width": 3},
            fill="tozeroy",
            fillcolor="rgba(79, 209, 197, 0.12)",
            name="PnL",
        )
    )
    figure.update_layout(
        margin={"l": 10, "r": 10, "t": 10, "b": 10},
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        showlegend=False,
    )
    figure.update_xaxes(showgrid=False, zeroline=False)
    figure.update_yaxes(gridcolor="rgba(140,163,191,0.12)", zeroline=False)

    st.plotly_chart(
        figure,
        use_container_width=True,
        config={"displayModeBar": False, "displaylogo": False},
    )

