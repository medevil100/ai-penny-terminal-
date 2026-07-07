from __future__ import annotations
import yfinance as yf
import pandas as pd
import numpy as np

class YahooService:
    """Zaawansowany serwis analityczny pobierający dane i obliczający wskaźniki techniczne."""

    def get_full_analysis(self, ticker: str) -> dict | None:
        """Pobiera dane historyczne i oblicza pełen zestaw wskaźników technicznych."""
        try:
            # Pobieramy rok danych, aby poprawnie wyliczyć EMA200 i ATR
            df = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=False)
            
            if df.empty or len(df) < 200:
                return None

            # Spłaszczenie indeksów kolumn yfinance (dla nowszych wersji biblioteki)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)

            # 1. Pobranie podstawowych danych OHLCV (ostatni pasek)
            last_row = df.iloc[-1]
            close_price = float(last_row['Close'])
            ohlc = {
                "Open": float(last_row['Open']),
                "High": float(last_row['High']),
                "Low": float(last_row['Low']),
                "Close": close_price
            }
            volume = int(last_row['Volume'])

            # 2. Obliczanie EMA (20, 50, 200)
            df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA200'] = df['Close'].ewm(span=200, adjust=False).mean()

            # 3. Obliczanie RSI (14)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
            loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
            rs = gain / (loss + 1e-10)
            df['RSI'] = 100 - (100 / (1 + rs))

            # 4. Obliczanie MACD (12, 26, 9)
            exp1 = df['Close'].ewm(span=12, adjust=False).mean()
            exp2 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = exp1 - exp2
            df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

            # 5. Obliczanie ATR (14)
            high_low = df['High'] - df['Low']
            high_close = np.abs(df['High'] - df['Close'].shift())
            low_close = np.abs(df['Low'] - df['Close'].shift())
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            true_range = ranges.max(axis=1)
            df['ATR'] = true_range.ewm(alpha=1/14, adjust=False).mean()

            # 6. Obliczanie VWAP (przybliżenie dzienno-wsteczne dla dziennego interwału)
            df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()

            # 7. Obliczanie RVOL (Relative Volume - Wolumen z dziś vs średnia z 20 dni)
            df['Vol_MA20'] = df['Volume'].rolling(window=20).mean()
            df['RVOL'] = df['Volume'] / (df['Vol_MA20'] + 1e-10)

            # Pobranie najświeższych obliczonych wartości
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
            print(f"Błąd YahooService: {e}")
            return None
