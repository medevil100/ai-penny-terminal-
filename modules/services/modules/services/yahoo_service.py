from __future__ import annotations
import yfinance as yf
import pandas as pd
import numpy as np

class YahooService:
    """Zaawansowany serwis analityczny pobierający dane i obliczający wskaźniki techniczne."""

    def get_full_analysis(self, ticker: str) -> dict | None:
        """Pobiera dane historyczne i oblicza pełen zestaw wskaźników technicznych."""
        try:
            # Próba pobrania standardowego roku danych
            ticker_obj = yf.Ticker(ticker)
            df = ticker_obj.history(period="1y", interval="1d", actions=False, auto_adjust=True)
            
            # --- TRYB RATUNKOWY DLA MAŁO PŁYNNYCH SPÓŁEK/GROSZÓWEK ---
            # Jeśli tabela jest pusta, próbujemy pobrać krótszy okres (np. ostatnie 3 miesiące)
            if df.empty or len(df) < 5:
                df = ticker_obj.history(period="3mo", interval="1d", actions=False, auto_adjust=True)
                
            # Jeśli po próbie ratunkowej nadal nie ma danych, walor nie istnieje w Yahoo Finance
            if df.empty or len(df) < 3:
                return None

            # Standaryzacja i ujednolicenie nazw nagłówków kolumn
            df.columns = [str(col).strip().capitalize() for col in df.columns]

            # Wymuszenie formatu numerycznego dla kluczowych danych giełdowych
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Uzupełniamy ewentualne puste dni (brak obrotu na groszówkach) poprzednimi wartościami
            df = df.ffill().dropna(subset=['Close'])

            # Pobranie bazowych danych OHLCV z ostatniej sesji
            last_row = df.iloc[-1]
            close_price = float(last_row['Close'])
            ohlc = {
                "Open": float(last_row['Open']),
                "High": float(last_row['High']),
                "Low": float(last_row['Low']),
                "Close": close_price
            }
            volume = int(last_row['Volume']) if 'Volume' in df.columns else 0

            # --- OBLICZENIA WSKAŹNIKÓW Z DYNAMICZNYMI WAGAMI (Dopasowane do długości historii) ---
            history_len = len(df)
            
            df['EMA20'] = df['Close'].ewm(span=min(20, history_len), adjust=False).mean()
            df['EMA50'] = df['Close'].ewm(span=min(50, history_len), adjust=False).mean()
            df['EMA200'] = df['Close'].ewm(span=min(200, history_len), adjust=False).mean()

            # Obliczanie RSI (14) lub krótszego, jeśli historia jest bardzo krótka
            rsi_period = min(14, history_len - 1) if history_len > 2 else 2
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).ewm(alpha=1/rsi_period, adjust=False).mean()
            loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/rsi_period, adjust=False).mean()
            rs = gain / (loss + 1e-10)
            df['RSI'] = 100 - (100 / (1 + rs))

            # Obliczanie MACD
            exp1 = df['Close'].ewm(span=min(12, history_len), adjust=False).mean()
            exp2 = df['Close'].ewm(span=min(26, history_len), adjust=False).mean()
            df['MACD'] = exp1 - exp2
            df['Signal'] = df['MACD'].ewm(span=min(9, history_len), adjust=False).mean()

            # Obliczanie ATR
            high_low = df['High'] - df['Low']
            high_close = np.abs(df['High'] - df['Close'].shift())
            low_close = np.abs(df['Low'] - df['Close'].shift())
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            true_range = ranges.max(axis=1)
            df['ATR'] = true_range.ewm(alpha=1/rsi_period, adjust=False).mean()

            # Obliczanie VWAP
            df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / (df['Volume'].cumsum() + 1e-10)

            # Obliczanie RVOL (Wolumen dzisiejszy vs średnia z dostępnych dni, max 20)
            vol_period = min(20, history_len)
            df['Vol_MA20'] = df['Volume'].rolling(window=vol_period, min_periods=1).mean()
            df['RVOL'] = df['Volume'] / (df['Vol_MA20'] + 1e-10)

            # Pobranie najświeższych obliczonych rekordów
            last_calculated = df.iloc[-1]

            return {
                "ticker": ticker,
                "price": close_price,
                "ohlc": ohlc,
                "volume": volume,
                "rsi": float(last_calculated['RSI']),
                "ema20": float(last_calculated['EMA20']),
                "ema50": float(last_calculated['EMA50']),
                "ema200": float(last_calculated['EMA200']),
                "macd": float(last_calculated['MACD']),
                "macd_signal": float(last_calculated['Signal']),
                "atr": float(last_calculated['ATR']),
                "vwap": float(last_calculated['VWAP']),
                "rvol": float(last_calculated['RVOL'])
            }

        except Exception as e:
            print(f"Błąd krytyczny YahooService: {e}")
            return None
