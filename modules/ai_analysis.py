import sys
from pathlib import Path
from .services.yahoo_service import YahooService
from .services.ai_prompt import build_prompt


# Wymuszenie dodania głównego katalogu projektu, aby Python zawsze widział folder 'services'
root_path = Path(__file__).parent.parent.absolute()
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# Dopiero teraz mogą nastąpić pozostałe importy
import streamlit as st
import json
import requests
from services.yahoo_service import YahooService
from services.ai_prompt import build_prompt

def fetch_tavily_news(ticker: str) -> list:
    """Pobiera do 10 newsów rynkowych, komunikaty i insider data przez Tavily API."""
    try:
        tavily_key = st.secrets["TAVILY_API_KEY"]
        url = "https://tavily.com"
        payload = {
            "api_key": tavily_key,
            "query": f"{ticker} stock news earnings reports insider sentiment",
            "search_depth": "advanced",
            "max_results": 10,
            "include_answer": False
        }
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            results = response.json().get("results", [])
            return [{"title": r.get("title"), "content": r.get("content"), "url": r.get("url")} for r in results]
    except Exception:
        pass
    return [{"title": "Brak danych newsowych", "content": "Nie udało się pobrać komunikatów dla tego waloru."}]

def send_telegram_alert(message: str):
    """Wysyła gotowy raport sygnałowy bezpośrednio na Twój kanał Telegram."""
    try:
        bot_token = st.secrets["TELEGRAM_BOT_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]
        url = f"https://telegram.org{bot_token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}, timeout=5)
    except Exception:
        pass

def run():
    st.title("🤖 AI Analysis Center v1.0")
    st.write("Profesjonalny system skanowania groszówek zintegrowany z Yahoo, Tavily oraz OpenAI.")

    # --- INPUT UŻYTKOWNIKA ---
    col_input, col_horizon = st.columns(2)
    with col_input:
        ticker = st.text_input("Ticker spółki (np. BML.WA, TSLA):", value="BML.WA").upper()
    with col_horizon:
        horizon = st.selectbox("Horyzont Swing:", ["Krótkoterminowy (1-2 tygodnie)", "Średnioterminowy (2-6 tygodni)", "Długoterminowy (powyżej 6 tygodni)"])

    if st.button("🚀 Uruchom pełną analizę AI"):
        
        # --- SEKCIJA SPINNERÓW I LOGÓW (Prawdziwe wywołania systemowe) ---
        st.subheader("📝 Logi systemowe")
        log_box = st.empty()
        
        # 1. YAHOO FINANCE
        with st.spinner("Łączenie z Yahoo Finance..."):
            log_box.code(f"Yahoo Finance Service: Pobieranie danych historycznych dla {ticker}...")
            yahoo = YahooService()
            indicators = yahoo.get_full_analysis(ticker)
            
            if not indicators:
                st.error(f"❌ Nie udało się pobrać lub wyliczyć wskaźników OHLC/RSI/MACD/EMA dla tickera {ticker}. Sprawdź poprawność symbolu.")
                return
                
            log_box.code(f"Yahoo Finance Service: Obliczono pomyślnie [Cena: {indicators['price']} PLN | RSI: {indicators['rsi']:.2f} | RVOL: {indicators['rvol']:.2f}x]")

        # 2. TAVILY SEARCH
        with st.spinner("Uruchamianie Tavily Search (Pobieranie 10 newsów, earnings, insider)..."):
            log_box.code("Tavily Search: Przeszukiwanie sieci, pobieranie ostatnich 10 komunikatów i raportów...")
            news_data = fetch_tavily_news(ticker)
            log_box.code(f"Tavily Search: Pobrano pomyślnie {len(news_data)} komunikatów giełdowych.")

        # 3. OPENAI PLATFORM
        with st.spinner("Wysyłanie zapytania do OpenAI Platform (Analiza matematyczno-behawioralna)..."):
            log_box.code("OpenAI Platform: Kompilowanie promptu analitycznego (150 linii) i uruchamianie LLM...")
            
            if not openai_client:
                st.error("❌ Brak skonfigurowanego klucza OPENAI_API_KEY w sekretach Streamlit.")
                return

            prompt = build_prompt(ticker, indicators, news_data, horizon)
            
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.2
                )
                ai_result = json.loads(response.choices[0].message.content)
                log_box.code("OpenAI Platform: Analiza strukturalna JSON wygenerowana bez błędów.")
            except Exception as e:
                st.error(f"❌ Błąd krytyczny OpenAI: {e}")
                return

        # 4. TELEGRAM ALERT
        with st.spinner("Generowanie powiadomienia Telegram Alert..."):
            log_box.code("Telegram Alert: Formatowanie skróconego raportu sygnałowego...")
            
            tg_message = (
                f"🚨 *Sygnał Swing AI: {ticker}*\n"
                f"🎯 Decyzja: {ai_result.get('decision')}\n"
                f"📊 AI Score: {ai_result.get('total_score')}/100\n"
                f"⏳ Horyzont: {horizon}\n\n"
                f"🎯 TP1: {ai_result.get('tp1')} PLN\n"
                f"🎯 TP2: {ai_result.get('tp2')} PLN\n"
                f"🎯 TP3: {ai_result.get('tp3')} PLN\n"
                f"🛑 Stop Loss: {ai_result.get('sl')} PLN"
            )
            send_telegram_alert(tg_message)
            log_box.code("Telegram Alert: Raport został wysłany na Twój kanał giełdowy.")

        st.success("✅ Pełna analiza rynkowa zakończona sukcesem!")
        st.divider()

        # --- SEKCIJA INTERFEJSU UŻYTKOWNIKA (Dynamiczne Streamlit UI) ---
        st.subheader(f"📊 Wynik analizy dla: {ticker}")

        # Główne wskaźniki zasilone z AI
        c1, c2, c3 = st.columns(3)
        c1.metric("Decyzja AI", ai_result.get("decision"), delta=f"Pewność: {ai_result.get('confidence_pct')}%")
        c2.metric("Sentyment rynkowy", ai_result.get("sentiment_label"))
        c3.metric("Poziom Ryzyka", ai_result.get("risk_level"))

        st.info(f"⏳ **Zakładany horyzont inwestycyjny:** {horizon}")

        # --- POTĘŻNY DYNAMICZNY AI SCORE BOARD ---
        st.markdown(f"### 🏆 AI SCORE: {ai_result.get('total_score')} / 100")
        
        # Paski postępu odzwierciedlające punkty przyznane przez OpenAI
        st.progress(min(ai_result.get("total_score", 0) / 100, 1.0))
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.write(f"📈 **Trend:** +{ai_result.get('score_trend')} / 20")
            st.write(f"🔊 **Volume (RVOL):** +{ai_result.get('score_volume')} / 15")
            st.write(f"🎛️ **RSI:** +{ai_result.get('score_rsi')} / 10")
        with col_s2:
            st.write(f"📊 **MACD:** +{ai_result.get('score_macd')} / 15")
            st.write(f"📰 **News:** +{ai_result.get('score_news')} / 20")
            st.write(f"👥 **Sentiment:** +{ai_result.get('score_sentiment')} / 12")

        st.divider()

        # Sekcje komentarzy opisowych pobranych z JSON od OpenAI
        st.markdown("### 📈 Analiza Trendu (Yahoo Finance)")
        st.write(ai_result.get("trend_comment"))

        st.markdown("### 📰 Podsumowanie Wiadomości i Komunikatów (Tavily)")
        st.write(ai_result.get("news_comment"))

        st.markdown("### 📝 Komentarz i Strategia (OpenAI Platform)")
        st.write(ai_result.get("ai_analysis_comment"))

        st.markdown("### ⚠️ Czynniki Ryzyka")
        st.write(ai_result.get("risk_comment"))

        # Docelowe poziomy cenowe przeniesione na sam dół raportu
        st.markdown("## ━━━━━━━━━━━━━━━━━━━━")
        st.markdown("### 🎯 Docelowe poziomy cenowe (Sygnał Swing)")
        
        st.success(f"🎯 **TP1 (Take Profit 1):** {ai_result.get('tp1'):.2f} PLN")
        st.success(f"🎯 **TP2 (Take Profit 2):** {ai_result.get('tp2'):.2f} PLN")
        st.success(f"🎯 **TP3 (Take Profit 3):** {ai_result.get('tp3'):.2f} PLN")
        st.error(f"🛑 **STOP LOSS (SL):** {ai_result.get('sl'):.2f} PLN")

        st.caption("Powyższy raport został wygenerowany automatycznie przez silnik AI Penny Terminal na podstawie analizy matematyczno-behawioralnej.")
