import streamlit as st
import yfinance as yf
import pandas as pd


def run():

    st.title("🇵🇱 GPW Scanner")

    tickers_text = st.text_area(
        "Wpisz tickery (przecinki):",
        "BML.WA, BCX.WA, GRN.WA"
    )

    if st.button("🚀 Skanuj"):

        tickers = [
            x.strip().upper()
            for x in tickers_text.split(",")
            if x.strip()
        ]

        results = []

        progress = st.progress(0)

        for i, ticker in enumerate(tickers):

            try:
                stock = yf.Ticker(ticker)

                df = stock.history(
                    period="1mo",
                    interval="1d"
                )

                if not df.empty:

                    last = df.iloc[-1]
                    prev = df.iloc[-2]

                    change = (
                        (last["Close"] - prev["Close"])
                        / prev["Close"]
                    ) * 100

                    results.append({
                        "Ticker": ticker,
                        "Cena": round(float(last["Close"]), 3),
                        "Zmiana %": round(float(change), 2),
                        "Wolumen": int(last["Volume"])
                    })

            except Exception as e:
                pass

            progress.progress(
                (i + 1) / len(tickers)
            )

        if results:

            table = pd.DataFrame(results)

            table = table.sort_values(
                "Zmiana %",
                ascending=False
            )

            st.dataframe(
                table,
                use_container_width=True
            )

        else:

            st.warning(
                "Nie znaleziono danych."
            )
