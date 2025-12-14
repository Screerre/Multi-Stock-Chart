import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ---------------- CONFIG PAGE ----------------
st.set_page_config(
    page_title="Comparateur de Sous-Jacents",
    layout="wide"
)

st.title("📈 Comparateur de sous-jacents")
st.markdown("Entrez des **noms de compagnies, tickers Yahoo ou ISIN**")

# ---------------- DICTIONNAIRE NOM → TICKER ----------------
COMPANY_TO_TICKER = {
    "nvidia": "NVDA",
    "apple": "AAPL",
    "microsoft": "MSFT",
    "tesla": "TSLA",
    "amazon": "AMZN",
    "meta": "META",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "bnp": "BNP.PA",
    "bnp paribas": "BNP.PA",
    "total": "TTE.PA",
    "lvmh": "MC.PA"
}

def normalize_to_ticker(user_input: str):
    x = user_input.strip().lower()
    if x in COMPANY_TO_TICKER:
        return COMPANY_TO_TICKER[x]
    return user_input.strip().upper()

# ---------------- INTERFACE ----------------
nb_sj = st.number_input("Nombre de sous-jacents", min_value=1, max_value=10, value=2)

sous_jacents = {}
for i in range(nb_sj):
    name = st.text_input(f"Sous-jacent {i+1} - Nom / Ticker / ISIN", key=f"ticker{i}")
    date = st.date_input(f"Sous-jacent {i+1} - Date", key=f"date{i}")
    sous_jacents[i] = {"input": name, "date": date}

if st.button("📊 Générer le graphique"):
    data = {}
    tickers_detected = []

    for i in range(nb_sj):
        user_input = sous_jacents[i]["input"]
        date = sous_jacents[i]["date"]
        if not user_input:
            continue
        ticker = normalize_to_ticker(user_input)
        tickers_detected.append(ticker)
        try:
            df = yf.download(ticker, start=date, end=date + timedelta(days=1), progress=False)
            if not df.empty:
                data[ticker] = pd.Series([df["Close"].iloc[0]], index=[date])
        except Exception:
            st.warning(f"Impossible de récupérer {ticker}")

    if not data:
        st.error("Aucune donnée récupérée.")
    else:
        st.subheader("📌 Tickers détectés")
        st.write(", ".join(tickers_detected))

        df_prices = pd.DataFrame(data)

        # ---------------- GRAPH ----------------
        fig, ax = plt.subplots(figsize=(12, 5))
        for col in df_prices.columns:
            ax.plot(df_prices.index, df_prices[col], marker='o', label=col)

        ax.set_title("Évolution des sous-jacents")
        ax.set_xlabel("Date")
        ax.set_ylabel("Prix")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)
        st.success("Graphique généré avec succès ✅")
