from __future__ import annotations  # Ta linia MUSI być na samym początku pliku
"""
=========================================================
AI Penny Terminal
Yahoo Finance Service
=========================================================
"""

import yfinance as yf
import pandas as pd


class YahooService:
    """Serwis odpowiedzialny za pobieranie danych z Yahoo Finance."""

    def get_history(
        self,
        ticker: str,
        period: str = "6mo",
        interval: str = "1d",
    ) -> pd.DataFrame:
        """Pobiera dane historyczne dla jednego tickera."""
        try:
            df = yf.download(
                ticker,
                period=period,
                interval=interval,
                progress=False,
                auto_adjust=False,
            )

            if df.empty:
                return pd.DataFrame()

            return df

        except Exception as e:
            print(e)
            return pd.DataFrame()

    def get_last_price(self, ticker: str):
        df = self.get_history(
            ticker=ticker,
            period="5d",
            interval="1d",
        )

        if df.empty:
            return None

        # Konwersja na typ float z obsługą struktur wielopoziomowych w nowym yfinance
        try:
            val = df["Close"].iloc[-1]
            return float(val.iloc[0]) if hasattr(val, "iloc") else float(val)
        except Exception:
            return None

    def get_volume(self, ticker: str):
        df = self.get_history(
            ticker,
            period="5d",
        )

        if df.empty:
            return None

        try:
            val = df["Volume"].iloc[-1]
            return int(val.iloc[0]) if hasattr(val, "iloc") else int(val)
        except Exception:
            return None
