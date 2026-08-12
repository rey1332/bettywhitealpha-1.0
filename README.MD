# BettyWhite Alpha

BettyWhite is a modular market dashboard.

## Features

- Candlestick chart with VWAP and TWAP overlays
- Watchlist, positions, and PnL panels
- AI signal cards derived from current market state
- News and auction-market placeholder panels for future live feeds
- Provider/service split designed for future Sierra Chart integration

## Quick Start

1. Create a virtual environment.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Launch the dashboard:

```bash
streamlit run app.py
```

## Project Layout

```text
app.py
bettywhite_alpha/
  analytics/
  data/
  domain/
  integrations/
  services/
  ui/
.streamlit/config.toml
requirements.txt
```

## Integration Path

The UI reads from `DashboardService`, which depends on a `MarketDataProvider`. The included `MockMarketDataProvider` generates realistic sample data. To plug in Sierra Chart later, implement the methods in `bettywhite_alpha/integrations/sierra_chart.py` and swap the provider used in `app.py`.

