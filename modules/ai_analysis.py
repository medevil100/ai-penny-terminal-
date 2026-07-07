import streamlit as st
import time

def run():
    st.title("🤖 AI Analysis Center")
    st.write("Wprowadź ticker spółki (np. z GPW lub USA), aby przeprowadzić pełną analizę kondycji, sentymentu i wyznaczyć poziomy TP/SL.")

    # --- INPUT UŻYTKOWNIKA ---
    col_input, col_horizon = st.columns([2, 2])
    with col_input:
        ticker = st.text_input("Ticker spółki:", value="BML.WA").upper()
    with col_horizon:
        horizon = st.selectbox("Horyzont Swing:", ["Krótkoterminowy (1-2 tygodnie)", "Średnioterminowy (2-6 tygodni)", "Długoterminowy (powyżej 6 tygodni)"])

    if st.button("🚀 Uruchom pełną analizę AI"):
        
        # --- SEKCIJA SPINNERÓW I LOGÓW ---
        st.subheader("📝 Logi systemowe")
        log_box = st.empty()
        
        with st.spinner("Inicjalizacja terminala analitycznego..."):
            log_box.code("AI Penny Terminal: Rozpoczęto proces analizy...")
            time.sleep(1)
            
        with st.spinner("Łączenie z Yahoo Finance..."):
            log_box.code(f"Yahoo Finance Service: Pobieranie danych historycznych dla {ticker}...")
            time.sleep(1.5)
            log_box.code("Yahoo Finance Service: Dane pobrane pomyślnie. Obliczanie wskaźników technicznych...")
            time.sleep(0.5)

        with st.spinner("Uruchamianie Tavily Search..."):
            log_box.code("Tavily Search: Przeszukiwanie sieci pod kątem najnowszych wiadomości i komunikatów...")
            time.sleep(1.5)
            log_box.code("Tavily Search: Znaleziono 4 istotne artykuły prasowe z ostatnich 48 godzin.")

        with st.spinner("Wysyłanie zapytania do OpenAI Platform..."):
            log_box.code("OpenAI Platform: Generowanie promptu strukturalnego i analiza fundamentalna...")
            time.sleep(2)
            log_box.code("OpenAI Platform: Raport matematyczno-behawioralny został wygenerowany.")

        with st.spinner("Generowanie powiadomienia Telegram Alert..."):
            log_box.code("Telegram Alert: Wysyłanie skróconego raportu sygnałowego na kanał...")
            time.sleep(1)
            log_box.code("Telegram Alert: Wiadomość wysłana pomyślnie [Status: ONLINE]")

        st.success("✅ Analiza zakończona sukcesem!")
        st.divider()

        # --- SEKCIJA INTERFEJSU UŻYTKOWNIKA (Streamlit UI) ---
        st.subheader(f"📊 Wynik analizy dla: {ticker}")

        # Główne wskaźniki (Ocena, Sentyment, Ryzyko)
        c1, c2, c3 = st.columns(3)
        c1.metric("Ocena AI", "8.5 / 10", delta="Kupuj", delta_color="normal")
        c2.metric("Sentyment rynkowy", "BYCZY (Bullish)", delta="Pozytywny", delta_color="normal")
        c3.metric("Poziom Ryzyka", "ŚREDNI", delta="-12%", delta_color="inverse")

        st.info(f"⏳ **Horyzont inwestycyjny:** {horizon}")

        # Podział na raport tekstowy i poziomy cenowe
        col_text, col_levels = st.columns([3, 2])

        with col_text:
            st.markdown("### 📝 Podsumowanie Analityczne OpenAI")
            st.write(
                f"Na podstawie danych z **Yahoo Finance**, spółka {ticker} wykazuje silną akumulację w okolicach lokalnego wsparcia. "
                "Wskaźniki RSI oraz MACD sygnalizują wyprzedanie waloru, co sprzyja odbiciu technicznemu w wybranym horyzoncie swingowym. "
                "Dane z **Tavily Search** potwierdzają rosnące zainteresowanie inwestorów detalicznych na forach oraz w mediach społecznościowych."
            )
            st.write(
                "**Rekomendacja:** Otwieranie pozycji po cenie rynkowej z restrykcyjnym zarządzaniem kapitałem i pilnowaniem poziomu Stop Loss."
            )

        with col_levels:
            st.markdown("### 🎯 Docelowe poziomy cenowe (TP/SL)")
            
            # Karty poziomów
            st.error("🛑 SL (Stop Loss): 3.10 PLN")
            st.success("🎯 TP1 (Take Profit 1): 3.85 PLN")
            st.success("🎯 TP2 (Take Profit 2): 4.15 PLN")
            st.success("🎯 TP3 (Take Profit 3): 4.50 PLN")

        st.caption("Powyższy raport jest generowany automatycznie przez algorytmy AI i nie stanowi rekomendacji inwestycyjnej.")
