import streamlit as st
import pandas as pd
import pydeck as pdk
import random
from datetime import date
import hashlib

# ==============================================================================
# RIVAPRO – L’app ultra precisa per la pesca da riva responsabile in Italia
# ==============================================================================

st.set_page_config(
    page_title="RivaPro – Pesca da Riva Responsabile",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎣 RivaPro – Pesca da Riva Responsabile 🌿")

# -------------------------------- SIDEBAR -------------------------------------
st.sidebar.header("Filtri Pesca")

selected_date = st.sidebar.date_input("Data pesca", date.today())

technique = st.sidebar.selectbox(
    "Tecnica di pesca",
    ["Tutte", "Surfcasting", "Pesca a fondo dagli scogli/porto", "Bolognese", "Spinning"]
)

is_premium = st.sidebar.checkbox("Modalità Premium attiva", value=False)

# -------------------------------- SPOT LIST – TUTTA ITALIA -----------------------------------
spots = [
    # Liguria (esempi completi con esche uniche)
    {'name': 'Sanremo Scogliere', 'lat': 43.8167, 'lon': 7.7667, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Spinning'], 'premium': False, 'esche': ['Gambero vivo', 'Polpo fresco', 'Verme americano'], 'percentuali': {'Gambero vivo': 50, 'Polpo fresco': 30, 'Verme americano': 20}},
    {'name': 'Porto Venere Molo', 'lat': 44.0500, 'lon': 9.8333, 'techniques': ['Bolognese', 'Spinning'], 'premium': False, 'esche': ['Bigattino', 'Cozza sgusciata', 'Arenicola'], 'percentuali': {'Bigattino': 45, 'Cozza sgusciata': 35, 'Arenicola': 20}},
    {'name': 'Cinque Terre Calette', 'lat': 44.1333, 'lon': 9.7167, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Calamaro', 'Polpo', 'Sardina filetto'], 'percentuali': {'Calamaro': 50, 'Polpo': 30, 'Sardina filetto': 20}},
    {'name': 'Levanto Molo', 'lat': 44.1667, 'lon': 9.6167, 'techniques': ['Bolognese', 'Surfcasting'], 'premium': False, 'esche': ['Arenicola king', 'Cozza', 'Gambero'], 'percentuali': {'Arenicola king': 45, 'Cozza': 30, 'Gambero': 25}},
    {'name': 'Imperia Porto', 'lat': 43.8833, 'lon': 8.0333, 'techniques': ['Spinning', 'Bolognese'], 'premium': False, 'esche': ['Minnow artificiale', 'Sardina', 'Verme'], 'percentuali': {'Minnow artificiale': 50, 'Sardina': 30, 'Verme': 20}},
    {'name': 'Alassio Spiaggia', 'lat': 44.0000, 'lon': 8.1667, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Bibi', 'Cozza', 'Americano'], 'percentuali': {'Bibi': 50, 'Cozza': 30, 'Americano': 20}},
    {'name': 'Varazze Scogliere', 'lat': 44.3667, 'lon': 8.5833, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': True, 'esche': ['Polpo', 'Calamaro', 'Gambero'], 'percentuali': {'Polpo': 45, 'Calamaro': 35, 'Gambero': 20}},
    {'name': 'Savona Diga', 'lat': 44.3000, 'lon': 8.4833, 'techniques': ['Spinning'], 'premium': True, 'esche': ['Gamberetto', 'Sardina', 'Verme'], 'percentuali': {'Gamberetto': 50, 'Sardina': 30, 'Verme': 20}},
    {'name': 'Genova Pegli', 'lat': 44.4167, 'lon': 8.8167, 'techniques': ['Surfcasting', 'Bolognese'], 'premium': True, 'esche': ['Cozza', 'Arenicola', 'Gambero'], 'percentuali': {'Cozza': 40, 'Arenicola': 35, 'Gambero': 25}},
    {'name': 'Camogli Scogli', 'lat': 44.3500, 'lon': 9.1500, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': True, 'esche': ['Sardina', 'Polpo', 'Verme'], 'percentuali': {'Sardina': 40, 'Polpo': 30, 'Verme': 30}},

    # Toscana (esempi)
    {'name': 'Porto Mediceo, Livorno', 'lat': 43.5510, 'lon': 10.3015, 'techniques': ['Surfcasting', 'Bolognese'], 'premium': False, 'esche': ['Arenicola', 'Cozza', 'Gambero'], 'percentuali': {'Arenicola': 45, 'Cozza': 35, 'Gambero': 20}},
    {'name': 'Spiaggia del Felciaio, Livorno', 'lat': 43.5218, 'lon': 10.3170, 'techniques': ['Spinning', 'Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Verme', 'Sardina', 'Gamberetto'], 'percentuali': {'Verme': 40, 'Sardina': 30, 'Gamberetto': 30}},
    # ... (aggiungi tutti gli altri spot con 'esche' e 'percentuali' unici, come sopra)

    # Abruzzo e Marche (come richiesto)
    {'name': 'Pescara Molo Nord', 'lat': 42.4694, 'lon': 14.2156, 'techniques': ['Bolognese', 'Spinning'], 'premium': False, 'esche': ['Verme', 'Gambero', 'Cozza'], 'percentuali': {'Verme': 40, 'Gambero': 35, 'Cozza': 25}},
    {'name': 'Ortona Porto', 'lat': 42.3567, 'lon': 14.4067, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Bolognese'], 'premium': False, 'esche': ['Polpo', 'Sardina', 'Arenicola'], 'percentuali': {'Polpo': 45, 'Sardina': 30, 'Arenicola': 25}},
    {'name': 'Vasto Punta Penna', 'lat': 42.1667, 'lon': 14.7167, 'techniques': ['Surfcasting', 'Spinning'], 'premium': False, 'esche': ['Gambero', 'Cozza', 'Verme'], 'percentuali': {'Gambero': 50, 'Cozza': 30, 'Verme': 20}},
    {'name': 'Torre Cerrano (Pineto)', 'lat': 42.5833, 'lon': 14.1000, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Arenicola', 'Sardina', 'Polpo'], 'percentuali': {'Arenicola': 45, 'Sardina': 35, 'Polpo': 20}},
    {'name': 'Fossacesia Marina Scogli', 'lat': 42.2333, 'lon': 14.5000, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Spinning'], 'premium': True, 'esche': ['Polpo', 'Gambero', 'Cozza'], 'percentuali': {'Polpo': 50, 'Gambero': 30, 'Cozza': 20}},

    {'name': 'Ancona Porto Antico', 'lat': 43.6200, 'lon': 13.5100, 'techniques': ['Bolognese', 'Spinning'], 'premium': False, 'esche': ['Verme', 'Gambero', 'Sardina'], 'percentuali': {'Verme': 40, 'Gambero': 35, 'Sardina': 25}},
    {'name': 'Senigallia Spiaggia di Velluto', 'lat': 43.7167, 'lon': 13.2167, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Arenicola', 'Cozza', 'Polpo'], 'percentuali': {'Arenicola': 45, 'Cozza': 30, 'Polpo': 25}},
    {'name': 'Fano Molo', 'lat': 43.8500, 'lon': 13.0167, 'techniques': ['Bolognese', 'Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Cozza', 'Verme', 'Gambero'], 'percentuali': {'Cozza': 40, 'Verme': 35, 'Gambero': 25}},
    {'name': 'Numana Riviera del Conero', 'lat': 43.5167, 'lon': 13.6167, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Spinning'], 'premium': True, 'esche': ['Polpo', 'Sardina', 'Arenicola'], 'percentuali': {'Polpo': 50, 'Sardina': 30, 'Arenicola': 20}},
    {'name': 'Grottammare Lungomare Sud', 'lat': 42.9833, 'lon': 13.8667, 'techniques': ['Surfcasting', 'Spinning'], 'premium': True, 'esche': ['Gambero', 'Verme', 'Cozza'], 'percentuali': {'Gambero': 45, 'Verme': 35, 'Cozza': 20}},
]

# (Il resto del codice è identico alla versione precedente – funzioni, mappa, report con voce 4 premium % cattura)

# In generate_fishing_info, voce 4:
info += f"""
**4. Esche consigliate + prede possibili + pastura**  
1. {spot['esche'][0]} {"(" + str(spot['percentuali'][spot['esche'][0]]) + "%)" if is_premium else ""}  
2. {spot['esche'][1]} {"(" + str(spot['percentuali'][spot['esche'][1]]) + "%)" if is_premium else ""}  
3. {spot['esche'][2]} {"(" + str(spot['percentuali'][spot['esche'][2]]) + "%)" if is_premium else ""}  
Prede principali: Orata, Sarago, Spigola, Ombrina, Grongo.  
Pastura: sardine macinate + pane, 5kg a 50m.
"""

# Programma con arrivo variabile (1h prima picco solunare)
peak_hour = int(solunar['time'].split('-')[0].split(':')[0])
arrival_hour = peak_hour - 1 if peak_hour > 1 else peak_hour + 11  # Evita negativo
info += f"""
**5. Programma di pesca completo**  
Orario di arrivo consigliato: {arrival_hour}:00 (1h prima picco solunare)  
Fase 1: Setup e pasturazione  
Fase 2: Primi lanci all'alba o tramonto  
Fase 3: Picco attività {solunar['time']} – controlli frequenti  
Fase 4: Pesca fino al calare del sole o chiusura notturna  
Chiusura sessione: entro le 22:00 o alba successiva
"""

st.markdown("***Messaggio green:*** Porta via i tuoi rifiuti e, se puoi, anche quelli altrui. Un vero pescatore protegge il suo spot 🌿")
st.caption("RivaPro – Pesca da Riva Responsabile 🇮🇹 | Versione aggiornata 2026")
