from __future__ import annotations

import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bw-bg-0: #050b14;
            --bw-bg-1: #0b1726;
            --bw-panel: rgba(12, 24, 38, 0.92);
            --bw-panel-strong: rgba(14, 28, 43, 0.97);
            --bw-border: rgba(149, 186, 222, 0.16);
            --bw-text: #f4f7fb;
            --bw-muted: #8ca3bf;
            --bw-accent: #4fd1c5;
            --bw-warm: #f7b955;
            --bw-danger: #ff6b6b;
        }

        html, body, [class*="css"] {
            font-family: "Space Grotesk", "Aptos", "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 0% 0%, rgba(79, 209, 197, 0.16), transparent 24%),
                radial-gradient(circle at 100% 0%, rgba(247, 185, 85, 0.12), transparent 22%),
                linear-gradient(180deg, #040a12 0%, #07111f 50%, #091524 100%);
            color: var(--bw-text);
        }

        [data-testid="stHeader"] {
            background: rgba(0, 0, 0, 0);
        }

        [data-testid="stSidebar"] {
            background: rgba(7, 14, 24, 0.95);
            border-right: 1px solid var(--bw-border);
        }

        [data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(14, 28, 43, 0.98), rgba(10, 20, 32, 0.9));
            border: 1px solid var(--bw-border);
            padding: 0.95rem 1rem;
            border-radius: 18px;
            box-shadow: 0 16px 34px rgba(0, 0, 0, 0.18);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--bw-muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.72rem;
            font-weight: 600;
        }

        div[data-testid="stMetricValue"] {
            color: var(--bw-text);
            font-weight: 700;
        }

        .stPlotlyChart, [data-testid="stDataFrame"] {
            background: linear-gradient(180deg, rgba(14, 28, 43, 0.98), rgba(10, 20, 32, 0.92));
            border: 1px solid var(--bw-border);
            border-radius: 18px;
            padding: 0.35rem;
            box-shadow: 0 16px 34px rgba(0, 0, 0, 0.18);
        }

        .bw-hero {
            padding: 0.2rem 0 0.8rem 0;
        }

        .bw-title {
            margin: 0;
            color: #ffffff;
            font-size: 2.35rem;
            line-height: 1.05;
            font-weight: 800;
            letter-spacing: -0.05em;
        }

        .bw-subtitle {
            margin: 0.45rem 0 0 0;
            color: var(--bw-muted);
            max-width: 62rem;
            font-size: 0.98rem;
            line-height: 1.5;
        }

        .bw-badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
            margin-top: 1rem;
        }

        .bw-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            border: 1px solid var(--bw-border);
            background: rgba(11, 22, 34, 0.88);
            color: var(--bw-text);
            font-size: 0.82rem;
        }

        .bw-section-title {
            margin: 0;
            color: var(--bw-text);
            font-size: 1rem;
            font-weight: 700;
            letter-spacing: 0.01em;
        }

        .bw-section-subtitle {
            margin: 0.18rem 0 0.9rem 0;
            color: var(--bw-muted);
            font-size: 0.86rem;
        }

        .bw-signal-card,
        .bw-placeholder-card,
        .bw-news-card {
            background: linear-gradient(180deg, rgba(14, 28, 43, 0.98), rgba(10, 20, 32, 0.93));
            border: 1px solid var(--bw-border);
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 16px 34px rgba(0, 0, 0, 0.18);
            margin-bottom: 0.8rem;
        }

        .bw-card-kicker {
            display: inline-block;
            color: var(--bw-muted);
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 600;
        }

        .bw-card-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.8rem;
        }

        .bw-card-title {
            margin: 0.35rem 0 0.15rem 0;
            color: var(--bw-text);
            font-size: 1.02rem;
            font-weight: 700;
        }

        .bw-card-copy {
            margin: 0.35rem 0 0 0;
            color: #c9d4e5;
            font-size: 0.9rem;
            line-height: 1.45;
        }

        .bw-card-foot {
            margin-top: 0.75rem;
            color: var(--bw-muted);
            font-size: 0.8rem;
        }

        .bw-pill {
            display: inline-flex;
            align-items: center;
            padding: 0.28rem 0.6rem;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .bw-pill.long,
        .bw-pill.aligned,
        .bw-pill.compression {
            background: rgba(79, 209, 197, 0.14);
            color: var(--bw-accent);
        }

        .bw-pill.short,
        .bw-pill.extended,
        .bw-pill.expansion,
        .bw-pill.fade {
            background: rgba(255, 107, 107, 0.14);
            color: var(--bw-danger);
        }

        .bw-pill.hold {
            background: rgba(247, 185, 85, 0.14);
            color: var(--bw-warm);
        }

        .bw-placeholder-list {
            margin: 0.55rem 0 0 1rem;
            color: #c9d4e5;
            padding: 0;
        }

        .bw-placeholder-list li {
            margin-bottom: 0.38rem;
            line-height: 1.4;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

