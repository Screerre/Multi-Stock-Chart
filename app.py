import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---------------- CONFIG PAGE ----------------
st.set_page_config(
    page_title="Comparateur de Performance",
    layout="wide"
)

st.title("📈 Comparateur de performance des sous-jacents")
st.markdown("Entrez des **noms de compagnies, tickers Yahoo ou ISIN** et leurs dates de début (DD/MM/YYYY)")

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

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%d/%m/%Y")
    except Exception:
        return None

# ---------------- INTERFACE ----------------
nb_sj = st.number_input("Nombre de sous-jacents", min_value=1, max_value=10, value=2)

sous_jacents = {}
for i in range(nb_sj):
    name = st.text_input(f"Sous-jacent {i+1} - Nom / Ticker / ISIN", key=f"ticker{i}")
    date_str = st.text_input(f"Sous-jacent {i+1} - Date de début (DD/MM/YYYY)", key=f"date{i}", placeholder="ex: 01/01/2020")
    sous_jacents[i] = {"input": name, "date_str": date_str}

if st.button("📊 Générer le graphique"):
    dfs = []
    tickers_detected = []

    for i in range(nb_sj):
        user_input = sous_jacents[i]["input"]
        date_str = sous_jacents[i]["date_str"]
        if not user_input or not date_str:
            continue

        start_date = parse_date(date_str)
        if not start_date:
            st.warning(f"Date invalide pour le sous-jacent {i+1} ({date_str})")
            continue

        ticker = normalize_to_ticker(user_input)
        tickers_detected.append(f"{ticker} ({start_date.strftime('%d/%m/%Y')})")

        try:
            start_date_yf = start_date.strftime("%Y-%m-%d")
            df = yf.download(ticker, start=start_date_yf, progress=False)
            if not df.empty:
                # Calcul de l'évolution normalisée à 100
                perf = 100 * df["Close"] / df["Close"].iloc[0]
                df_perf = perf.to_frame(name=ticker)
                dfs.append(df_perf)
            else:
                st.warning(f"Aucune donnée disponible pour {ticker} depuis {date_str}")
        except Exception as e:
            st.warning(f"Impossible de récupérer {ticker} ({e})")

    if not dfs:
        st.error("Aucune donnée récupérée.")
    else:
        st.subheader("📌 Tickers détectés")
        st.write(", ".join(tickers_detected))

        # Concaténer tous les DataFrames par date
        df_perf_all = pd.concat(dfs, axis=1)

        # ---------------- GRAPH ----------------
        fig, ax = plt.subplots(figsize=(12, 5))
        for col in df_perf_all.columns:
            ax.plot(df_perf_all.index, df_perf_all[col], label=col)

        ax.set_title("Performance relative des sous-jacents (100 = date de début)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Indice de performance")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)
        st.success("Graphique généré avec succès ✅")
