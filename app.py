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

st.title("<Comparateur de performance des sous-jacents>")
st.markdown("Entrez des **noms de compagnies, tickers Yahoo ou ISIN** et leurs dates de début (DD/MM/YYYY)")

# ---------------- DICTIONNAIRE NOM → TICKER ----------------
COMPANY_TO_TICKER = {
    
        "stmicroelectronics": "SGMR.DU", "infineon": "IFX.F","edenred": "OMUM.IL",
        "cac40": "^FCHI","cac 40": "^FCHI","cac": "^FCHI","eurostoxx": "^STOXX50E",
        "eurostox": "^STOXX50E","sx5e": "^STOXX50E","dowjones": "^DJI","dow jones": "^DJI",
        "ftse": "^FTSE","ftse100": "^FTSE","ftse 100": "^FTSE","nasdaq": "^IXIC",
        "APPLE": "AAPL", "MICROSOFT": "MSFT", "GOOGLE": "GOOGL", "ALPHABET": "GOOGL",
        "AMAZON": "AMZN","META": "META","BERKSHIRE HATHAWAY": "BRK-A","JOHNSON & JOHNSON": "JNJ",
        "JPMORGAN CHASE": "JPM", "EXXON MOBIL": "XOM", "COCA-COLA": "KO",
        "WALMART": "WMT", "DISNEY": "DIS", "LVMH": "LVMH.PA", "LOREAL": "OR.PA",
        "TOTALENERGIES": "TTE", "SANTE": "SAN.PA", "BNP PARIBAS": "BNP.PA",
        "BNP": "BNP.PA", "SOCIETE GENERALE": "GLE.PA", "HERMES": "RMS.PA",
        "AIRBUS": "AIR.PA", "AXA": "CS.PA", "SAP": "SAP.DE", "SIEMENS": "SIE.DE",
        "BAYER": "BAYN.DE", "SAMSUNG": "005930.KS", "TSMC": "TSM","TOYOTA": "TM",
        "JPMORGAN CHASE": "JPM","BANK OF AMERICA": "BAC",
        "WELLS FARGO & CO": "WFC","GOLDMAN SACHS": "GS","MORGAN STANLEY": "MS",
        "CITIGROUP INC": "C","CITIGROUP": "C","CITI" : "C","BNP PARIBAS": "BNP.PA",
        "CREDIT AGRICOLE": "ACA.PA","DEUTSCHE BANK AG": "DBK.DE","COMMERZBANK AG": "CBK.DE",
        "UBS GROUP AG": "UBSG.SW","UBS GROUP" : "UBSG.SW","UBS": "UBSG.SW"
        "STANDARD CHARTERED": "STAN.L","BARCLAYS PLC": "BARC.L","LLOYDS BANKING GROUP": "LLOY.L",
        "NATWEST GROUP": "NWG.L","ROYAL BANK OF CANADA": "RY","TORONTO-DOMINION BANK": "TD",
        "SOCIETE GENERALE": "GLE.PA","HSBC": "HSBA.L",
  # --- BANQUES RÉGIONALES ET SPÉCIALISÉES (US & EU) ---
        "PNC FINANCIAL SERV": "PNC","US BANCORP": "USB","CAPITAL ONE FINANCIAL": "COF",
        "ZIONS BANCORP": "ZION","COMERICA INC": "CMA","HUNTINGTON BANCSHARES": "HBAN",
        "REGIONS FINANCIAL CORP": "RF","FIFTH THIRD BANCORP": "FITB","KEYCORP": "KEY",
        "EAST WEST BANCORP": "EWBC","ING GROEP NV": "INGA.AS","KBC GROUP NV": "KBC.BR",
        "BANCO SANTANDER": "SAN","UNICREDIT SPA": "UCG.MI",
        "INTESA SANPAOLO": "ISP.MI","BANCO DE SABADELL": "SAB.MC","CAIXABANK SA": "CABK.MC",
        "MEDIOBANCA SPA": "MB.MI","NORDEA BANK ABP": "NDA-DK.CO",
        "DANSKE BANK A/S": "DANSKE.CO","SWEDBANK AB": "SWED A.ST","SEB AB": "SEB A.ST",
 # --- ASSURANCES (VIE, NON-VIE, RÉASSURANCE) ---
        "CHUBB LTD": "CB","AIG": "AIG","METLIFE INC": "MET","PRUDENTIAL FINANCIAL": "PRU",
        "UNUM GROUP": "UNM","TRUIST FINANCIAL CORP": "TFC","ALLIANZ SE": "ALV.DE",
        "MUNICH RE": "MUV2.DE","HANNOVER RE": "HNR1.DE","ZURICH INSURANCE GR": "ZURN.SW",
        "GENERALI ASSICURAZIONI": "G.MI","AVIVA PLC": "AV.L","LEGAL & GENERAL GR": "LGEN.L",
        "PRUDENTIAL PLC (UK)": "PRU.L","MANULIFE FINANCIAL": "MFC","SUN LIFE FINANCIAL": "SLF",
        "AXA SA": "CS.PA",
 # --- GESTION D'ACTIFS ET MARCHÉS DE CAPITAUX ---
       "BLACKROCK INC": "BLK","VANGUARD": "VTI","STATE STREET CORP": "STT","CME GROUP": "CME",
       "BANK OF NEW YORK MELLON": "BK","NORTHERN TRUST CORP": "NTRS","CME GROUP": "CME",
       "INTERCONTINENTAL EXC": "ICE","CBOE GLOBAL MARKETS": "CBOE","NASDAQ INC": "NDAQ",
       "LSE GROUP PLC": "LSEG.L","DEUTSCHE BOERSE AG": "DB1.DE","EURONEXT NV": "ENX.PA",
       "HONG KONG EXCHANGES": "0388.HK","S&P GLOBAL INC": "SPGI","MOODY'S CORP": "MCO",
       "FACTSET RESEARCH": "FDS",
 # --- FINTECH ET PAIEMENTS ---
       "VISA INC": "V","MASTERCARD INC": "MA","AMERICAN EXPRESS": "AXP", "FIS GLOBAL": "FIS",
       "PAYPAL HOLDINGS": "PYPL","SQUARE (BLOCK INC)": "SQ","COINBASE GLOBAL": "COIN",
       "ADYEN NV": "ADYEN.AS","GLOBAL PAYMENTS INC": "GPN","FISERV INC": "FISV",
       "FIS GLOBAL": "FIS","DISCOVER FINANCIAL SERV": "DFS","SYNCHRONY FINANCIAL": "SYF",
       "AFFIRM HOLDINGS": "AFRM","SOFI TECHNOLOGIES": "SOFI","ROBINHOOD MARKETS": "HOOD",
       "WISE PLC": "WISE.L","PAGSEGURO DIGITAL": "PAGS","STONECO LTD": "STNE", 
# -- BANQUES ASIATIQUES ET ÉMERGENTES --
       "MITSUBISHI UFJ FIN": "8306.T","SUMITOMO MITSUI FIN": "8316.T","MIZUHO FINANCIAL GR": "8411.T",
       "NOMURA HOLDINGS": "8604.T","HDFC BANK": "HDFCBANK.NS","ICICI BANK": "ICICIBANK.NS",
       "AXIS BANK": "AXISBANK.NS","STATE BANK OF INDIA": "SBIN.NS","BANK OF CHINA": "3988.HK",
       "CHINA CONSTRUCTION BK": "0939.HK","ICBC": "1398.HK","WESTPAC BANKING CORP": "WBC.AX",
       "ANZ GROUP HOLDINGS": "ANZ.AX","COMMONWEALTH BANK AUS": "CBA.AX","MACQUARIE GROUP": "MQG.AX",
       "DBS GROUP HOLDINGS": "DBSM.SI","OVERSEAS CHINESE BK": "OCBC.SI",
# -- BOITES IA ET TECH --
       "ARISTANETWORKS": "ANET","ACLARARES": "ACLA","ALPHA&OMEGASEMI": "AOSL","MONOLITHICPOWERSYS": "MPWR",
       "QORVOINC": "QRVO","LUMINARTECH": "LAZR","AMD": "AMD","GLOBO": "GLBE","AXCELISTECHNOLOGIES": "ACLS",
       "NOVARTUS": "NVTS","SILICONLABS": "SLAB","HIMAXTECHNOLOGIES": "HIMX","INPHICORPORATION": "IPHI",
       "ONSEMICONDUCTOR": "ON","MACOMTECHNOLOGY": "MTSI","MKSINSTRUMENTS": "MKSI","ULVAC": "6728.T",
       "OKTAINC": "OKTA","DATADOG": "DDOG","COUPASOFTWARE": "COUP","C3AI": "AI","UPSTARTHOLDINGS": "UPST",
       "VEEVASYSTEMS": "VEEV","ZENDESK": "ZEN","NEWRELIC": "NEWR","MULESOFT": "MULE","ASANA": "ASAN",
       "PALANTIRTECHNOLOGIES": "PLTR","DRAFTKINGS": "DKNG","CROWDSTRIKEHOLDINGS": "CRWD","ZSCALER": "ZS",
       "FORTINET": "FTNT","CHECKPOINTSOFTWARE": "CHKP","CYBERARKSOFTWARE": "CYBR","PROOFPOINT": "PFPT",
       "OKTA": "OKTA","ACTEURSASIATIQUES&EUROPÉENS": "","NORDICSEMICONDUCTOR": "NOD.OL","IMEC": "IMEC.BR",
       "ACCELERATED": "ACEL","INFINEONTECHNOLOGIES": "IFX.DE","STMICROELECTRONICS": "STM","JD.COM": "JD",
       "ASMLHOLDING": "ASML","MEITUAN": "3690.HK","JD.COM": "JD","BAIDUINC": "BIDU","NETEASEINC": "NTES",
       "SKHYNIX": "000660.KS","KINGSOFTCLOUD": "KC","SONYGROUPCORP": "SONY","CANONINC": "CAJ","REDHAT": "IBM",
       "ARCELIKAS": "ARCLK.IS","INVITAECORP": "NVTA","TAIYOYUDENCO": "6976.T","TOKYOELECTRONLTD": "8035.T",
       "SCREENHOLDINGSCO": "7735.T","BESEMICONDUCTOR": "BESI.AS","EVOTECSE": "EVT.DE","BIONTECHSE": "BNTX",
       "TELADOCHEALTH": "TDOC","MAXLINEARINC": "MXL","WIX.COMLTD": "WIX","RINGCENTRAL": "RNG",
       "PAYCOMSOFTWARE": "PAYC","DOCUSIGNINC": "DOCU","TERADATACORP": "TDC","DATTOHOLDINGCORP": "DATTO",
       "CHECKPOINTSOFT": "CHKP","PALOALTONETWORKS": "PANW","ASANAINC": "ASAN","FASTLYINC": "FSLY",
       "LATTICESEMICON": "LSCC","DURATIONMEDIA": "DUR","ROHMCOLTD": "6963.T","DISCOCORP": "6146.T",
       "PHOTRONLTD": "6899.T","AMS-OSRAMAG": "AMS.SW","SARTORIUSSTEDIM": "DIM.PA","CUREVACNV": "CVAC",
       "ACCELERATEDIAGNOSTICS": "AXDX","SAGEGROUPPLC": "SGE.L","HUBSPOTINC": "HUBS","CLOUDERA": "CLDR",
       "FIVERRINTERNATIONAL": "FVRR","AUTOMATICDATAPROC": "ADP","HEWLETTPACKARDENT": "HPE",
       "COUPASOFTWARE": "COUP","DXCTECHNOLOGY": "DXC","CYBERARKSOFTWARE": "CYBR","ZSCALERINC": "ZS",
       "C3.AIINC": "AI","CORTICELLIB": "CORB","CREEINC": "CREE","AMBARELLAINC": "AMBA","SUMCOCORP": "3436.T",
       "LASERTECCORP": "6920.T","ASMINTERNATIONAL": "ASM.AS","AIXTRONSE": "AIXA.DE","GENMABAS": "GMAB.CO",
       "VAXARTINC": "VXRT","INSIGHTENTERPRISES": "NSIT","AVEVAGROUPPLC": "AVV.L","ZILLOWGROUP": "Z",
       "OKTAINC": "OKTA","UPWORKINC": "UPWK","SALESFORCEINC": "CRM","DELLTECHNOLOGIES": "DELL",
       "PAGERDUTYINC": "PD","MICROFOCUSINTL": "MCRO.L","FORTINETINC": "FTNT","VEEVASYSTEMS": "VEEV",
       "ATOSSE": "ATOS.PA","UPSTARTHOLDINGS": "UPST","SUMOLOGIC": "SUMO","SPLUNKINC": "SPLK",
       "STMICROELECTRONICS": "SGMR.DU","INFINEON": "IFX.F",
  #--- CAC60  ---            
        "LVMH": "MC.PA","Hermes International": "RMS.PA",
       "L'Oreal": "OR.PA","Airbus": "AIR.PA","Schneider Electric": "SU.PA","EssilorLuxottica": "EL.PA",
       "Safran": "SAF.PA","TotalEnergies": "TTE.PA","Sanofi": "SAN.PA","Air Liquide": "AI.PA",
       "Vinci": "DG.PA","Engie": "ENGI.PA","Danone": "BN.PA","Thales": "HO.PA","Saint-Gobain": "SGO.PA",
       "Orange": "ORA.PA","Kering": "KER.PA","Legrand": "LR.PA","Dassault Systemes": "DSY.PA",
       "ArcelorMittal": "MT.AS","Stellantis": "STLAM.MI","Capgemini": "CAP.PA","Publicis Groupe": "PUB.PA",
       "Veolia Environnement": "VIE.PA","Dassault Aviation": "AM.PA","Sartorius Stedim Biotech": "DIM.PA",
       "STMicroelectronics": "STM.PA","Michelin": "ML.PA","Pernod Ricard": "RI.PA","Bouygues": "EN.PA",
       "Amundi": "AMUN.PA","Unibail-Rodamco-Westfield": "URW.PA","Aeroports de Paris": "ADP.PA",
       "bioMerieux": "BIM.PA","Euronext": "ENX.PA","Eiffage": "FGR.PA","Bureau Veritas": "BVI.PA",
       "Alstom": "ALO.PA","Accor": "AC.PA","Eurofins Scientific": "ERF.PA","Renault": "RNO.PA",
       "Carrefour": "CA.PA","Rexel": "RXL.PA","Klepierre": "LI.PA","Getlink": "GET.PA","SPIE": "SPIE.PA",
       "Sodexo": "SW.PA","Gecina": "GFC.PA","Gaztransport & Technigaz": "GTT.PA","Technip Energies": "TE.PA",
       "Nexans": "NEX.PA","Scor": "SCR.PA","Edenred": "EDEN.PA","Arkema": "AKE.PA",
#--- FTSE100 ---
       "AstraZeneca": "AZN.L","HSBC Holdings": "HSBA.L","Shell": "SHEL.L","Unilever": "ULVR.L",
       "BP": "BP.L","GlaxoSmithKline": "GSK.L","British American Tobacco": "BATS.L","Rio Tinto": "RIO.L",
       "Diageo": "DGE.L","RELX": "REL.L", "London Stock Exchange Group": "LSEG.L","Barclays": "BARC.L",
       "Lloyds Banking Group": "LLOY.L","NatWest Group": "NWG.L","Standard Chartered": "STAN.L",
       "Prudential": "PRU.L","Legal & General": "LGEN.L","Aviva": "AV.L","Schroders": "SDR.L",
       "Experian": "EXPN.L","Reckitt Benckiser": "RKT.L","Compass Group": "CPG.L","Next": "NXT.L",
        "Associated British Foods": "ABF.L","Ocado Group": "OCDO.L","Marks & Spencer": "MKS.L",
        "Tesco": "TSCO.L","J Sainsbury": "SBRY.L","Kingfisher": "KGF.L","Persimmon": "PSN.L",
        "Barratt Developments": "BDEV.L","Taylor Wimpey": "TW.L","Whitbread": "WTB.L",
        "InterContinental Hotels Group": "IHG.L","Rolls-Royce Holdings": "RR.L","BAE Systems": "BA.L",
        "Smiths Group": "SMIN.L","Halma": "HLMA.L","Spirax-Sarco Engineering": "SPX.L",
        "Ashtead Group": "AHT.L","Croda International": "CRDA.L", "Fresnillo": "FRES.L",
        "Anglo American": "AAL.L","Antofagasta": "ANTO.L","Glencore": "GLEN.L","Rentokil Initial": "RTO.L",
        "Severn Trent": "SVT.L","United Utilities": "UU.L","National Grid": "NG.L",
#--- DAX ---
        "SAP": "SAP.DE","Siemens": "SIE.DE","Allianz": "ALV.DE","Deutsche Telekom": "DTE.DE",
        "Mercedes-Benz Group": "MBG.DE","BMW": "BMW.DE","Volkswagen": "VOW3.DE",
        "Porsche Automobil Holding": "PAH3.DE","Porsche AG": "P911.DE","BASF": "BAS.DE",
        "Bayer": "BAYN.DE","Merck KGaA": "MRK.DE","Siemens Healthineers": "SHL.DE",
        "Siemens Energy": "ENR.DE","Infineon Technologies": "IFX.DE","RWE": "RWE.DE",
        "E.ON": "EOAN.DE","Heidelberg Materials": "HEI.DE","MTU Aero Engines": "MTX.DE",
        "Deutsche Post DHL": "DHL.DE","Deutsche Boerse": "DB1.DE","Munich Re": "MUV2.DE",
        "Hannover Re": "HNR1.DE","Commerzbank": "CBK.DE","Deutsche Bank": "DBK.DE",
        "Fresenius": "FRE.DE","Fresenius Medical Care": "FME.DE","Beiersdorf": "BEI.DE",
        "Henkel": "HEN3.DE","Continental": "CON.DE","Covestro": "1COV.DE","Symrise": "SY1.DE",
        "Puma": "PUM.DE","Zalando": "ZAL.DE","Delivery Hero": "DHER.DE","Qiagen": "QIA.DE",
        "Sartorius": "SRT3.DE","Vonovia": "VNA.DE","Brenntag": "BNR.DE",
        
        "Apple": "AAPL","Microsoft": "MSFT","Alphabet": "GOOGL","Amazon": "AMZN","Nvidia": "NVDA",
        "Tesla": "TSLA","Meta Platforms": "META","Berkshire Hathaway": "BRK-A","Johnson & Johnson": "JNJ",
        "UnitedHealth Group": "UNH","Pfizer": "PFE","Merck & Co": "MRK","AbbVie": "ABBV","Eli Lilly": "LLY",
        "Amgen": "AMGN","Exxon Mobil": "XOM","Chevron": "CVX","ConocoPhillips": "COP","Coca-Cola": "KO",
        "PepsiCo": "PEP","Procter & Gamble": "PG","Walmart": "WMT","Costco": "COST","McDonalds": "MCD",
        "Nike": "NKE","Home Depot": "HD","Disney": "DIS","JPMorgan Chase": "JPM","Bank of America": "BAC",
        "Wells Fargo": "WFC","Goldman Sachs": "GS","Morgan Stanley": "MS","Citigroup": "C","Charles Schwab": "SCHW",
        "Ally Financial": "ALLY","BlackRock": "BLK","State Street": "STT","BNY Mellon": "BK","Northern Trust": "NTRS",
        "Visa": "V","Mastercard": "MA","American Express": "AXP","PayPal": "PYPL","Block": "SQ","Coinbase": "COIN",
        "Adobe": "ADBE","Oracle": "ORCL","Salesforce": "CRM","ServiceNow": "NOW","Workday": "WDAY","Intuit": "INTU",
        "Snowflake": "SNOW","ASML Holding": "ASML","Samsung Electronics": "005930.KS","SK Hynix": "000660.KS",
        "AMD": "AMD","Applied Materials": "AMAT","Lam Research": "LRCX","KLA": "KLAC","Infineon Technologies": "IFX.DE",
        "STMicroelectronics": "STM.PA","Tencent Holdings": "0700.HK","Alibaba Group": "BABA","JD.com": "JD",
        "Meituan": "3690.HK","Baidu": "BIDU","NetEase": "NTES","Sony Group": "SONY","Nintendo": "7974.T",
        "SoftBank Group": "9984.T","Keyence": "6861.T","Hitachi": "6501.T","Fanuc": "6954.T",
        "Recruit Holdings": "6098.T","Toyota Motor": "TM","Nestle": "NESN.SW","Roche Holding": "ROG.SW",
        "Novartis": "NOVN.SW","Zurich Insurance Group": "ZURN.SW","Swiss Re": "SREN.SW","UBS Group": "UBSG.SW",
        "Schneider Electric": "SU.PA","Vinci": "DG.PA", "SAP": "SAP.DE","Siemens": "SIE.DE","Allianz": "ALV.DE",
        "Deutsche Telekom": "DTE.DE","BMW": "BMW.DE","Mercedes-Benz Group": "MBG.DE","Volkswagen": "VOW3.DE",
        "BASF": "BAS.DE","Bayer": "BAYN.DE","Munich Re": "MUV2.DE","HSBC Holdings": "HSBA.L",
        "Shell": "SHEL.L","BP": "BP.L","Unilever": "ULVR.L","Rio Tinto": "RIO.L","Diageo": "DGE.L",
        "London Stock Exchange Group": "LSEG.L"
    }

def normalize_to_ticker(user_input: str):
    x = user_input.strip().lower()
    return COMPANY_TO_TICKER.get(x, user_input.strip().upper())

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

if st.button("Générer le graphique"):
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
            df = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), progress=False)
            if df is not None and not df.empty and "Close" in df.columns:
                # forcer en Series avec squeeze
                close_series = df["Close"].squeeze()
                # Normaliser à 100
                perf = 100 * close_series / close_series.iloc[0]
                # Convertir en DataFrame si ce n'est pas déjà
                if isinstance(perf, pd.Series):
                    df_perf = perf.to_frame(name=ticker)
                else:
                    df_perf = pd.DataFrame(perf)
                dfs.append(df_perf)
            else:
                st.warning(f"Aucune donnée disponible pour {ticker} depuis {date_str}")
        except Exception as e:
            st.warning(f"Impossible de récupérer {ticker} ({e})")

    if not dfs:
        st.error("Aucune donnée récupérée.")
    else:
        st.subheader("Tickers détectés :")
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
