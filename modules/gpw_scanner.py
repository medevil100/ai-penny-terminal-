import streamlit as st
import yfinance as yf
import pandas as pd


def run():

    st.title("🇵🇱 GPW Scanner")

    tickers = st.text_input(
        "Tickery GPW (oddzielone przecinkami)",
        value="BML.WA, BCX.WA"
    )

    if st.button("🔍 Skanuj GPW"):

        lista = [x.strip().upper() for x in tickers.split(",") if x.strip()]

        wyniki = []

        for ticker in lista:

            try:

                df = yf.download(
                    ticker,
                    period="5d",
                    interval="1d",
                    progress=False
                )

                if df.empty:
                    continue

                close = float(df["Close"].iloc[-1])
                prev = float(df["Close"].iloc[-2])

                change = ((close - prev) / prev) * 100

                volume = int(df["Volume"].iloc[-1])

                wyniki.append({
                    "Ticker": ticker,
                    "Cena": round(close, 3),
                    "Zmiana %": round(change, 2),
                    "Wolumen": volume
                })

            except Exception:
                pass

        if wyniki:

            tabela = pd.DataFrame(wyniki)

            tabela = tabela.sort_values(
                by="Zmiana %",
                ascending=False
            )

            st.dataframe(
                tabela,
                use_container_width=True
            )

        else:

            st.warning("Brak danych.")
