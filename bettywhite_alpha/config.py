from __future__ import annotations

APP_TITLE = "BettyWhite Alpha"
APP_ICON = None

DEFAULT_SYMBOL = "ES"
DEFAULT_BARS = 240

SYMBOL_OPTIONS = [
    "ES",
    "NQ",
    "RTY",
    "CL",
    "GC",
    "EURUSD",
    "BTCUSD",
]

TIMEFRAME_OPTIONS = ["1m", "5m", "15m", "1H"]
SESSION_MODES = ["Execution", "Intraday", "Overnight"]

TIMEFRAME_TO_FREQ = {
    "1m": "1min",
    "5m": "5min",
    "15m": "15min",
    "1H": "1H",
}

SYMBOL_BASE_PRICES = {
    "ES": 5487.0,
    "NQ": 19325.0,
    "RTY": 2258.0,
    "CL": 77.8,
    "GC": 2442.0,
    "EURUSD": 1.094,
    "BTCUSD": 63750.0,
}

