import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---------------- CONFIG PAGE ----------------
st.set_page_config(
    page_title="Comparateur de Sous-Jacents",
    layout="wide"
)

st.title("📈 Comparateur de sous-jacents")
st.markdown("Entrez des **noms de compagnies, tickers Yahoo ou ISIN** (un par ligne)")

# ---------------- DICTIONNAIRE NOM → TICKER ----------------
# (tu peux l’enrichir avec le temps)
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
    """Convertit nom / ticker / isin vers un ticker Yahoo"""
    x = user_input.strip().lower()

    # Si c'est dans le dictionnaire
    if x in COMPANY_TO_TICKER:
        return COMPANY_TO_TICKER[x]

    # Sinon on suppose que c'est déjà un ticker Yahoo
    return user_input.strip().upper()

# ---------------- INTERFACE ----------------
inputs = st.text_area(
    "Sous-jacents (un par ligne)",
    height=150,
    placeholder="Ex:\nNvidia\nAAPL\nBNP.PA\nTesla"
)

start_date = st.date_input(
    "Date de début",
    value=datetime(2020, 1, 1)
)

if st.button("📊 Générer le graphique"):
    if not inputs.strip():
        st.warning("Veuillez entrer au moins un sous-jacent.")
    else:
        tickers_raw = [x for x in inputs.split("\n") if x.strip()]
        tickers = [normalize_to_ticker(x) for x in tickers_raw]

        st.subheader("📌 Tickers détectés")
        st.write(", ".join(tickers))

        data = {}

        for ticker in tickers:
            try:
                df = yf.download(
                    ticker,
                    start=start_date,
                    progress=False
                )
                if not df.empty:
                    data[ticker] = df["Close"]
            except Exception:
                pass

        if not data:
            st.error("Aucune donnée récupérée.")
        else:
            df_prices = pd.DataFrame(data)

            # ---------------- GRAPH ----------------
            fig, ax = plt.subplots(figsize=(12, 5))

            for col in df_prices.columns:
                ax.plot(df_prices.index, df_prices[col], label=col)

            ax.set_title("Évolution des sous-jacents")
            ax.set_xlabel("Date")
            ax.set_ylabel("Prix")
            ax.legend()
            ax.grid(True)

            st.pyplot(fig)

            st.success("Graphique généré avec succès ✅")
