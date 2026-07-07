def build_prompt(ticker: str, indicators: dict, news_data: list, horizon: str) -> str:
    """
    Rygorystyczny prompt strukturalny dla OpenAI.
    Bezwzględnie zmusza model do obliczenia realnych punktów AI SCORE zamiast zer.
    """
    
    # Bezpieczne przygotowanie wartości, aby uniknąć błędów struktur wewnątrz f-stringa
    try:
        price_val = f"{indicators.get('price', 0):.2f}"
        rsi_val = f"{indicators.get('rsi', 50):.2f}"
        rvol_val = f"{indicators.get('rvol', 1.0):.2f}"
        macd_val = f"{indicators.get('macd', 0):.4f}"
        msig_val = f"{indicators.get('macd_signal', 0):.4f}"
        ema20_val = f"{indicators.get('ema20', 0):.2f}"
        ema50_val = f"{indicators.get('ema50', 0):.2f}"
        ema200_val = f"{indicators.get('ema200', 0):.2f}"
        ohlc_val = str(indicators.get('ohlc', "Brak danych OHLC"))
    except Exception:
        price_val, rsi_val, rvol_val, macd_val, msig_val = "0", "50", "1", "0", "0"
        ema20_val, ema50_val, ema200_val, ohlc_val = "0", "0", "0", "Brak danych"

    prompt = f"""
Jesteś elitarnym i bezwzględnie precyzyjnym algorytmem tradingowym wyspecjalizowanym w analizie spółek groszowych (Penny Stocks) oraz strategiach typu Swing Trading.
Twoim kluczowym zadaniem jest obliczenie składowych punktowych oraz sumarycznego wskaźnika AI SCORE dla waloru: {ticker}.

[HORYZONT INWESTYCYJNY]: {horizon}

[DANE TECHNICZNE Z YAHOO FINANCE]:
- Aktualna Cena Zamknięcia: {price_val} PLN
- Wskaźnik RSI(14): {rsi_val}
- RVOL (Relative Volume - Wolumen względny): {rvol_val}x
- Linia MACD: {macd_val} | Linia Sygnałowa MACD: {msig_val}
- Średnie Kroczące: EMA20={ema20_val}, EMA50={ema50_val}, EMA200={ema200_val}
- Słownik OHLC: {ohlc_val}
- Wolumen obrotu: {indicators.get('volume', 0)}
- Wskaźnik ATR(14) (Zmienność): {indicators.get('atr', 0):.4f}
- Wskaźnik VWAP: {indicators.get('vwap', 0):.2f}

[DANE NEWSOWE I BEHAWIORALNE]:
{news_data}

[ZASADY SYSTEMU PUNKTACJI AI SCORE (SUMA MAX: 100 PUNKTÓW)]:
Musisz dokonać matematycznego wyliczenia i przypisać punkty w każdej kategori! ZAKAZUJE SIĘ WPISYWANIA WARTOŚCI 0, CHYBA ŻE WSKAŹNIK JEST SKRAJNIE NEGATYWNY.
1. score_trend (Waga: 0 do 20 pkt): Jeśli cena > EMA20 > EMA50 > EMA200 daj od 15 do 20 pkt. Jeśli cena pod średnimi, daj poniżej 5 pkt.
2. score_volume (Waga: 0 do 15 pkt): Jeśli RVOL > 1.5x, daj od 10 do 15 pkt (jest obrót!). Jeśli RVOL < 1.0x, daj poniżej 5 pkt.
3. score_rsi (Waga: 0 do 10 pkt): Wyznacz punkty na podstawie poziomu RSI. Wyprzedanie (RSI < 30) z odbiciem = 10 pkt. Wykupienie (RSI > 70) = 2 pkt.
4. score_macd (Waga: 0 do 15 pkt): Przecięcie od dołu linii sygnałowej = 12 do 15 pkt. Trend spadkowy na histogramie = poniżej 5 pkt.
5. score_news (Waga: 0 do 20 pkt): Oceń pobrane z Tavily wiadomości i earnings raporty. Pozytywne komunikaty = 15 do 20 pkt.
6. score_sentiment (Waga: 0 do 12 pkt): Ogólny nastrój tłumu rynkowego na podstawie newsów.

[KRYTYCZNE WYMAGANIE MATEMATYCZNE]:
Pole `total_score` MUSI być dokładną sumą arytmetyczną pól składowych! 
Wzór: total_score = score_trend + score_volume + score_rsi + score_macd + score_news + score_sentiment. Oblicz to matematycznie!

[WYMAGANIA FORMATOWANIA]:
Zwróć odpowiedź WYŁĄCZNIE jako czysty obiekt JSON. Nie dodawaj tekstu przed/po, ani znaczników typu ```json.

Oto wymagany szablon struktury JSON:
{{
    "score_trend": 14,
    "score_volume": 11,
    "score_rsi": 7,
    "score_macd": 12,
    "score_news": 15,
    "score_sentiment": 9,
    "total_score": 68,
    "decision": "KUPUJ / SPRZEDAJ / OBSERWUJ",
    "sentiment_label": "BYCZY (Bullish) / NIEDŹWIEDZI (Bearish) / NEUTRALNY",
    "risk_level": "NISKI / ŚREDNI / WYSOKI",
    "trend_comment": "Komentarz odnośnie trendu...",
    "news_comment": "Podsumowanie wiadomości z Tavily...",
    "ai_analysis_comment": "Pełna analiza strategiczna OpenAI...",
    "risk_comment": "Główne czynniki ryzyka...",
    "tp1": 0.00,
    "tp2": 0.00,
    "tp3": 0.00,
    "sl": 0.00,
    "confidence_pct": 75
}}
"""
    return prompt.strip()
