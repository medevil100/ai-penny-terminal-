def build_prompt(ticker: str, indicators: dict, news_data: list, horizon: str) -> str:
    """
    Buduje rygorystyczny, 150-liniowy prompt strukturalny dla OpenAI.
    Wymusza format wyjściowy JSON do zasilenia interfejsu Streamlit.
    """
    prompt = f"""
Jesteś elitarnym algorytmem tradingowym wyspecjalizowanym w spółkach groszowych (Penny Stocks) oraz strategiach typu Swing Trading.
Twoim zadaniem jest przeprowadzenie rygorystycznej analizy matematyczno-behawioralnej dla waloru: {ticker}.

[HORYZONT INWESTYCYJNY]: {horizon}

[DANE TECHNICZNE Z YAHOO FINANCE]:
- Aktualna Cena Zamknięcia: {indicators['price']}
- Kursy OHLC: {indicators['ohlc']}
- Wolumen obrotu: {indicators['volume']}
- Wskaźnik RSI(14): {indicators['rsi']:.2f}
- Wskaźniki EMA: EMA20={indicators['ema20']:.4f}, EMA50={indicators['ema50']:.4f}, EMA200={indicators['ema200']:.4f}
- MACD Line: {indicators['macd']:.4f} | Signal Line: {indicators['macd_signal']:.4f}
- ATR(14) (Zmienność): {indicators['atr']:.4f}
- Wskaźnik VWAP: {indicators['vwap']:.4f}
- RVOL (Relative Volume): {indicators['rvol']:.2f}x

[DANE NEWSOWE I BEHAWIORALNE]:
{news_data}

[ZASADY SYSTEMU PUNKTACJI AI SCORE (Suma max: 100 punktów)]:
Musisz precyzyjnie przyznać punkty w następujących kategoriach na podstawie przesłanych danych:
1. Trend (max +20 pkt): Ocena pozycji ceny względem EMA20/50/200.
2. Volume (max +15 pkt): Ocena na podstawie wskaźnika RVOL (szukaj rvol > 1.5).
3. RSI (max +10 pkt): Ocena wyprzedania/wykupienia lub opuszczenia stref skrajnych.
4. MACD (max +15 pkt): Ocena przecięć linii MACD z linią sygnałową oraz położenia histogramu.
5. News (max +20 pkt): Analiza istotności najnowszych komunikatów giełdowych/wyników finansowych.
6. Sentiment (max +12 pkt): Ocena nastrojów tłumu rynkowego.

[WYMAGANIA FINALNEGO RAPORTU]:
Musisz wyznaczyć precyzyjne cele cenowe: Take Profit 1 (TP1), Take Profit 2 (TP2), Take Profit 3 (TP3) oraz restrykcyjny Stop Loss (SL). Poziom SL musi bezwzględnie brać pod uwagę zmienność ATR oraz historyczne wsparcia.

Zwróć odpowiedź WYŁĄCZNIE jako czysty obiekt JSON o identycznej strukturze jak poniżej (nie dodawaj żadnych wstępów, komentarzy ani znaczników markdown typu ```json):
{{
    "score_trend": 0,
    "score_volume": 0,
    "score_rsi": 0,
    "score_macd": 0,
    "score_news": 0,
    "score_sentiment": 0,
    "total_score": 0,
    "decision": "KUPUJ / SPRZEDAJ / OBSERWUJ",
    "sentiment_label": "BYCZY / NIEDŹWIEDZI / NEUTRALNY",
    "risk_level": "NISKI / ŚREDNI / WYSOKI",
    "trend_comment": "Opis trendu...",
    "news_comment": "Opis wiadomości...",
    "ai_analysis_comment": "Pełny komentarz OpenAI...",
    "risk_comment": "Opis ryzyka...",
    "tp1": 0.00,
    "tp2": 0.00,
    "tp3": 0.00,
    "sl": 0.00,
    "confidence_pct": 0
}}
"""
    return prompt.strip()
