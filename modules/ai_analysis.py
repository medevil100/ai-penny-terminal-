import streamlit as st
from openai import OpenAI
import yfinance as yf

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def run():

    st.title("🤖 AI Analysis")

    ticker = st.text_input(
        "Ticker",
        "STX.WA"
    ).upper()

    if st.button("🤖 Analizuj"):

        stock = yf.Ticker(ticker)

       try:

    if "last_scan" not in st.session_state:

    st.warning("Najpierw uruchom GPW Scanner.")

    return

df = st.session_state["last_scan"][ticker]

except Exception as e:

    st.error("Yahoo Finance chwilowo odrzuciło zapytanie.")

    st.info(
        "Odczekaj chwilę lub spróbuj ponownie."
    )

    return 

        if df.empty:

            st.error("Brak danych.")

            return

        last = df.iloc[-1]

        prompt = f"""
Przeanalizuj spółkę.

Ticker:
{ticker}

Cena:
{last['Close']:.4f}

High:
{last['High']:.4f}

Low:
{last['Low']:.4f}

Volume:
{int(last['Volume'])}

Odpowiedz jako trader.

Podaj:

Trend

Kupno

Take Profit

Stop Loss

Ryzyko

Komentarz
"""

        with st.spinner("AI analizuje..."):

            response = client.chat.completions.create(

                model="gpt-4o-mini",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]

            )

        st.success("Analiza gotowa")

        st.write(response.choices[0].message.content)
