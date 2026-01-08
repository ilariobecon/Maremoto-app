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

# -------------------------------- SPOT LIST – TUTTA ITALIA (completa) -----------------------------------
spots = [
    # Liguria
    {'name': 'Sanremo Scogliere', 'lat': 43.8167, 'lon': 7.7667, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Spinning'], 'premium': False, 'esche': ['Gambero vivo', 'Polpo fresco', 'Verme americano'], 'percentuali': {'Gambero vivo': 50, 'Polpo fresco': 30, 'Verme americano': 20}, 'prede': ['Spigola', 'Sarago', 'Orata', 'Grongo'], 'pastura': 'Pastura leggera con sardina macinata e formaggio'},
    {'name': 'Porto Venere Molo', 'lat': 44.0500, 'lon': 9.8333, 'techniques': ['Bolognese', 'Spinning'], 'premium': False, 'esche': ['Bigattino', 'Cozza sgusciata', 'Arenicola'], 'percentuali': {'Bigattino': 45, 'Cozza sgusciata': 35, 'Arenicola': 20}, 'prede': ['Sarago', 'Orata', 'Spigola', 'Mormora'], 'pastura': 'Pastura fine con pane e sarda per bolognese'},
    {'name': 'Cinque Terre Calette', 'lat': 44.1333, 'lon': 9.7167, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Calamaro', 'Polpo', 'Sardina filetto'], 'percentuali': {'Calamaro': 50, 'Polpo': 30, 'Sardina filetto': 20}, 'prede': ['Grongo', 'Sarago', 'Ombrina', 'Sgombro'], 'pastura': 'Pasturazione con calamaro e polpo per fondo profondo'},
    {'name': 'Levanto Molo', 'lat': 44.1667, 'lon': 9.6167, 'techniques': ['Bolognese', 'Surfcasting'], 'premium': False, 'esche': ['Arenicola king', 'Cozza', 'Gambero'], 'percentuali': {'Arenicola king': 45, 'Cozza': 30, 'Gambero': 25}, 'prede': ['Orata', 'Sarago', 'Spigola', 'Triglia'], 'pastura': 'Pastura densa con sardina e pane per surfcasting'},
    {'name': 'Imperia Porto', 'lat': 43.8833, 'lon': 8.0333, 'techniques': ['Spinning', 'Bolognese'], 'premium': False, 'esche': ['Minnow artificiale', 'Sardina', 'Verme'], 'percentuali': {'Minnow artificiale': 50, 'Sardina': 30, 'Verme': 20}, 'prede': ['Spigola', 'Sarago', 'Orata', 'Cefalo'], 'pastura': 'Pastura minima – spinning puro'},
    {'name': 'Alassio Spiaggia', 'lat': 44.0000, 'lon': 8.1667, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Bibi', 'Cozza', 'Americano'], 'percentuali': {'Bibi': 50, 'Cozza': 30, 'Americano': 20}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Sgombro'], 'pastura': 'Pastura con bibi e sardina per lunghe distanze'},
    {'name': 'Varazze Scogliere', 'lat': 44.3667, 'lon': 8.5833, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': True, 'esche': ['Polpo', 'Calamaro', 'Gambero'], 'percentuali': {'Polpo': 45, 'Calamaro': 35, 'Gambero': 20}, 'prede': ['Grongo', 'Ombrina', 'Sarago', 'Triglia'], 'pastura': 'Pasturazione con polpo tagliato per fondo'},
    {'name': 'Savona Diga', 'lat': 44.3000, 'lon': 8.4833, 'techniques': ['Spinning'], 'premium': True, 'esche': ['Gamberetto', 'Sardina', 'Verme'], 'percentuali': {'Gamberetto': 50, 'Sardina': 30, 'Verme': 20}, 'prede': ['Spigola', 'Sarago', 'Cefalo', 'Grongo'], 'pastura': 'Nessuna pastura – spinning puro'},
    {'name': 'Genova Pegli', 'lat': 44.4167, 'lon': 8.8167, 'techniques': ['Surfcasting', 'Bolognese'], 'premium': True, 'esche': ['Cozza', 'Arenicola', 'Gambero'], 'percentuali': {'Cozza': 40, 'Arenicola': 35, 'Gambero': 25}, 'prede': ['Orata', 'Sarago', 'Spigola', 'Mormora'], 'pastura': 'Pastura mista sardina e formaggio'},
    {'name': 'Camogli Scogli', 'lat': 44.3500, 'lon': 9.1500, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': True, 'esche': ['Sardina', 'Polpo', 'Verme'], 'percentuali': {'Sardina': 40, 'Polpo': 30, 'Verme': 30}, 'prede': ['Grongo', 'Ombrina', 'Sgombro', 'Triglia'], 'pastura': 'Pasturazione con sardina e polpo per rockfishing'},

    # Toscana
    {'name': 'Porto Mediceo, Livorno', 'lat': 43.5510, 'lon': 10.3015, 'techniques': ['Surfcasting', 'Bolognese'], 'premium': False, 'esche': ['Arenicola', 'Cozza', 'Gambero'], 'percentuali': {'Arenicola': 45, 'Cozza': 35, 'Gambero': 20}, 'prede': ['Orata', 'Sarago', 'Spigola', 'Mormora'], 'pastura': 'Pastura con arenicola e pane per surfcasting'},
    {'name': 'Spiaggia del Felciaio, Livorno', 'lat': 43.5218, 'lon': 10.3170, 'techniques': ['Spinning', 'Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Verme', 'Sardina', 'Gamberetto'], 'percentuali': {'Verme': 40, 'Sardina': 30, 'Gamberetto': 30}, 'prede': ['Spigola', 'Sarago', 'Orata', 'Cefalo'], 'pastura': 'Pastura leggera con gamberetto per spinning'},
    {'name': 'Cala del Leone, Livorno', 'lat': 43.4785, 'lon': 10.3205, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Surfcasting'], 'premium': False, 'esche': ['Polpo', 'Cozza', 'Arenicola'], 'percentuali': {'Polpo': 40, 'Cozza': 30, 'Arenicola': 30}, 'prede': ['Grongo', 'Ombrina', 'Sarago', 'Triglia'], 'pastura': 'Pasturazione con polpo e cozza per fondo'},
    {'name': 'Bocca d’Arno, Pisa', 'lat': 43.6790, 'lon': 10.2710, 'techniques': ['Spinning', 'Bolognese'], 'premium': False, 'esche': ['Gambero', 'Verme', 'Sardina'], 'percentuali': {'Gambero': 50, 'Verme': 30, 'Sardina': 20}, 'prede': ['Spigola', 'Orata', 'Sarago', 'Sgombro'], 'pastura': 'Pastura fine con bigattino per bolognese'},
    {'name': 'Spiaggia Marina di Cecina', 'lat': 43.2985, 'lon': 10.4805, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Arenicola', 'Cozza', 'Gambero'], 'percentuali': {'Arenicola': 40, 'Cozza': 35, 'Gambero': 25}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Cefalo'], 'pastura': 'Pastura densa con sardina e formaggio'},
    {'name': 'Buca delle Fate, Populonia', 'lat': 42.9950, 'lon': 10.4980, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Spinning'], 'premium': False, 'esche': ['Sardina', 'Verme', 'Polpo'], 'percentuali': {'Sardina': 40, 'Verme': 30, 'Polpo': 30}, 'prede': ['Grongo', 'Sarago', 'Ombrina', 'Triglia'], 'pastura': 'Pasturazione con sardina e polpo per fondo'},
    {'name': 'Golfo di Baratti', 'lat': 42.9900, 'lon': 10.5050, 'techniques': ['Surfcasting', 'Bolognese'], 'premium': False, 'esche': ['Gambero', 'Arenicola', 'Cozza'], 'percentuali': {'Gambero': 45, 'Arenicola': 35, 'Cozza': 20}, 'prede': ['Orata', 'Sarago', 'Spigola', 'Mormora'], 'pastura': 'Pastura mista sardina e pane per surfcasting'},
    {'name': 'Porto Ercole, Argentario', 'lat': 42.3930, 'lon': 11.2070, 'techniques': ['Spinning', 'Pesca a fondo dagli scogli/porto'], 'premium': True, 'esche': ['Verme', 'Gamberetto', 'Sardina'], 'percentuali': {'Verme': 40, 'Gamberetto': 30, 'Sardina': 30}, 'prede': ['Spigola', 'Sarago', 'Orata', 'Cefalo'], 'pastura': 'Pastura leggera con gamberetto per spinning'},
    {'name': 'Cala Violina', 'lat': 42.8433, 'lon': 10.7833, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Arenicola', 'Cozza', 'Polpo'], 'percentuali': {'Arenicola': 50, 'Cozza': 30, 'Polpo': 20}, 'prede': ['Orata', 'Mormora', 'Sarago', 'Triglia'], 'pastura': 'Pastura con arenicola e formaggio per lunghe distanze'},
    {'name': 'Follonica Puntone', 'lat': 42.9167, 'lon': 10.7667, 'techniques': ['Surfcasting', 'Bolognese'], 'premium': True, 'esche': ['Sardina', 'Gambero', 'Verme'], 'percentuali': {'Sardina': 40, 'Gambero': 30, 'Verme': 30}, 'prede': ['Spigola', 'Orata', 'Grongo', 'Sgombro'], 'pastura': 'Pastura densa con sardina e pane'},
    {'name': 'Talmoncino Spiaggia', 'lat': 42.6500, 'lon': 11.1000, 'techniques': ['Spinning'], 'premium': True, 'esche': ['Gambero', 'Verme', 'Sardina'], 'percentuali': {'Gambero': 50, 'Verme': 30, 'Sardina': 20}, 'prede': ['Spigola', 'Sarago', 'Ombrina', 'Cefalo'], 'pastura': 'Pastura minima – spinning puro'},
    {'name': 'Porto Santo Stefano', 'lat': 42.4333, 'lon': 11.1167, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': True, 'esche': ['Cozza', 'Polpo', 'Arenicola'], 'percentuali': {'Cozza': 40, 'Polpo': 30, 'Arenicola': 30}, 'prede': ['Grongo', 'Sarago', 'Orata', 'Triglia'], 'pastura': 'Pasturazione con polpo tagliato per fondo'},

    # Lazio (11 spot)
    {'name': 'Anzio Neronian Pier', 'lat': 41.4448, 'lon': 12.6295, 'techniques': ['Bolognese', 'Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Verme', 'Gambero', 'Cozza'], 'percentuali': {'Verme': 40, 'Gambero': 35, 'Cozza': 25}, 'prede': ['Sarago', 'Orata', 'Spigola', 'Mormora'], 'pastura': 'Pastura fine con bigattino per bolognese'},
    {'name': 'Fiumicino Mouth of Tiber', 'lat': 41.7675, 'lon': 12.2370, 'techniques': ['Surfcasting', 'Spinning'], 'premium': False, 'esche': ['Arenicola', 'Sardina', 'Gambero'], 'percentuali': {'Arenicola': 50, 'Sardina': 30, 'Gambero': 20}, 'prede': ['Spigola', 'Orata', 'Mormora', 'Cefalo'], 'pastura': 'Pastura densa con sardina per surfcasting'},
    {'name': 'Santa Marinella Beach', 'lat': 42.0320, 'lon': 11.8665, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Cozza', 'Arenicola', 'Verme'], 'percentuali': {'Cozza': 40, 'Arenicola': 35, 'Verme': 25}, 'prede': ['Orata', 'Sarago', 'Spigola', 'Triglia'], 'pastura': 'Pastura con cozza e pane per lunghe distanze'},
    {'name': 'Circeo Promontorio', 'lat': 41.2333, 'lon': 13.0667, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Polpo', 'Sardina', 'Gambero'], 'percentuali': {'Polpo': 40, 'Sardina': 30, 'Gambero': 30}, 'prede': ['Grongo', 'Ombrina', 'Sarago', 'Sgombro'], 'pastura': 'Pasturazione con polpo per fondo profondo'},
    {'name': 'Sabaudia Spiaggia', 'lat': 41.3000, 'lon': 13.0167, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Arenicola', 'Cozza', 'Sardina'], 'percentuali': {'Arenicola': 45, 'Cozza': 35, 'Sardina': 20}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Cefalo'], 'pastura': 'Pastura con arenicola e formaggio'},
    {'name': 'Ladispoli Scogliere', 'lat': 41.9500, 'lon': 12.0667, 'techniques': ['Spinning'], 'premium': False, 'esche': ['Gamberetto', 'Verme', 'Polpo'], 'percentuali': {'Gamberetto': 50, 'Verme': 30, 'Polpo': 20}, 'prede': ['Spigola', 'Sarago', 'Grongo', 'Triglia'], 'pastura': 'Pastura minima – spinning puro'},
    {'name': 'Riva di Traiano', 'lat': 42.1000, 'lon': 11.7667, 'techniques': ['Bolognese'], 'premium': True, 'esche': ['Verme', 'Gambero', 'Cozza'], 'percentuali': {'Verme': 40, 'Gambero': 30, 'Cozza': 30}, 'prede': ['Sarago', 'Orata', 'Spigola', 'Mormora'], 'pastura': 'Pastura fine con bigattino e pane'},
    {'name': 'Ostia Lido', 'lat': 41.7333, 'lon': 12.2667, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Sardina', 'Arenicola', 'Gambero'], 'percentuali': {'Sardina': 40, 'Arenicola': 30, 'Gambero': 30}, 'prede': ['Spigola', 'Mormora', 'Orata', 'Cefalo'], 'pastura': 'Pastura densa con sardina per lunghe distanze'},
    {'name': 'Torvaianica', 'lat': 41.6333, 'lon': 12.4667, 'techniques': ['Surfcasting', 'Spinning'], 'premium': True, 'esche': ['Cozza', 'Verme', 'Sardina'], 'percentuali': {'Cozza': 40, 'Verme': 30, 'Sardina': 30}, 'prede': ['Orata', 'Sarago', 'Spigola', 'Triglia'], 'pastura': 'Pastura mista cozza e sardina'},
    {'name': 'Nettuno Porto', 'lat': 41.4500, 'lon': 12.6667, 'techniques': ['Bolognese'], 'premium': True, 'esche': ['Gambero', 'Polpo', 'Arenicola'], 'percentuali': {'Gambero': 50, 'Polpo': 30, 'Arenicola': 20}, 'prede': ['Sarago', 'Grongo', 'Spigola', 'Sgombro'], 'pastura': 'Pastura con gambero e sardina per bolognese'},
    {'name': 'Gaeta Scogli', 'lat': 41.2000, 'lon': 13.5667, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': True, 'esche': ['Sardina', 'Verme', 'Cozza'], 'percentuali': {'Sardina': 40, 'Verme': 30, 'Cozza': 30}, 'prede': ['Grongo', 'Ombrina', 'Sarago', 'Cefalo'], 'pastura': 'Pasturazione con sardina per fondo profondo'},

    # Campania (11 spot)
    {'name': 'Palinuro Scogliere', 'lat': 40.0333, 'lon': 15.2833, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Spinning'], 'premium': False, 'esche': ['Polpo', 'Gambero', 'Verme'], 'percentuali': {'Polpo': 40, 'Gambero': 30, 'Verme': 30}, 'prede': ['Grongo', 'Spigola', 'Sarago', 'Triglia'], 'pastura': 'Pasturazione con polpo tagliato per fondo'},
    {'name': 'Acciaroli Porto', 'lat': 40.1833, 'lon': 15.0333, 'techniques': ['Bolognese'], 'premium': False, 'esche': ['Cozza', 'Sardina', 'Arenicola'], 'percentuali': {'Cozza': 40, 'Sardina': 30, 'Arenicola': 30}, 'prede': ['Sarago', 'Orata', 'Spigola', 'Cefalo'], 'pastura': 'Pastura fine con cozza e pane per bolognese'},
    {'name': 'Pozzuoli Porto', 'lat': 40.8167, 'lon': 14.1167, 'techniques': ['Spinning', 'Surfcasting'], 'premium': False, 'esche': ['Gamberetto', 'Verme', 'Sardina'], 'percentuali': {'Gamberetto': 50, 'Verme': 30, 'Sardina': 20}, 'prede': ['Spigola', 'Sarago', 'Grongo', 'Mormora'], 'pastura': 'Pastura leggera con gamberetto per spinning'},
    {'name': 'Cilento Costa', 'lat': 40.2000, 'lon': 15.0000, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Arenicola', 'Cozza', 'Polpo'], 'percentuali': {'Arenicola': 40, 'Cozza': 35, 'Polpo': 25}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Sgombro'], 'pastura': 'Pastura con arenicola e sardina per lunghe distanze'},
    {'name': 'Agropoli Molo', 'lat': 40.3500, 'lon': 14.9833, 'techniques': ['Bolognese'], 'premium': False, 'esche': ['Verme', 'Gambero', 'Sardina'], 'percentuali': {'Verme': 40, 'Gambero': 30, 'Sardina': 30}, 'prede': ['Sarago', 'Orata', 'Grongo', 'Triglia'], 'pastura': 'Pastura fine con bigattino per bolognese'},
    {'name': 'Salerno Lungomare', 'lat': 40.6667, 'lon': 14.7667, 'techniques': ['Spinning'], 'premium': False, 'esche': ['Gambero', 'Verme', 'Cozza'], 'percentuali': {'Gambero': 50, 'Verme': 30, 'Cozza': 20}, 'prede': ['Spigola', 'Sarago', 'Orata', 'Cefalo'], 'pastura': 'Pastura minima – spinning puro'},
    {'name': 'Amalfi Scogli', 'lat': 40.6333, 'lon': 14.6000, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': True, 'esche': ['Polpo', 'Sardina', 'Gambero'], 'percentuali': {'Polpo': 40, 'Sardina': 30, 'Gambero': 30}, 'prede': ['Grongo', 'Ombrina', 'Sarago', 'Sgombro'], 'pastura': 'Pasturazione con polpo per fondo profondo'},
    {'name': 'Castellabate Spiaggia', 'lat': 40.2833, 'lon': 14.9500, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Arenicola', 'Cozza', 'Verme'], 'percentuali': {'Arenicola': 40, 'Cozza': 30, 'Verme': 30}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Triglia'], 'pastura': 'Pastura con arenicola e formaggio'},
    {'name': 'Napoli Bay Scogliere', 'lat': 40.8333, 'lon': 14.2500, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': True, 'esche': ['Sardina', 'Gambero', 'Polpo'], 'percentuali': {'Sardina': 40, 'Gambero': 30, 'Polpo': 30}, 'prede': ['Sarago', 'Grongo', 'Spigola', 'Cefalo'], 'pastura': 'Pasturazione con sardina per fondo'},
    {'name': 'Ischia Porto', 'lat': 40.7333, 'lon': 13.9500, 'techniques': ['Bolognese'], 'premium': True, 'esche': ['Cozza', 'Verme', 'Arenicola'], 'percentuali': {'Cozza': 50, 'Verme': 30, 'Arenicola': 20}, 'prede': ['Sarago', 'Orata', 'Spigola', 'Mormora'], 'pastura': 'Pastura fine con cozza per bolognese'},
    {'name': 'Sorrento Punta', 'lat': 40.6167, 'lon': 14.3667, 'techniques': ['Spinning'], 'premium': True, 'esche': ['Gambero', 'Sardina', 'Verme'], 'percentuali': {'Gambero': 40, 'Sardina': 30, 'Verme': 30}, 'prede': ['Spigola', 'Sarago', 'Grongo', 'Sgombro'], 'pastura': 'Pastura minima – spinning puro'},

    # Puglia (12 spot)
    {'name': 'Vieste Gargano', 'lat': 41.8833, 'lon': 16.1667, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Spinning'], 'premium': False, 'esche': ['Polpo', 'Gambero', 'Verme'], 'percentuali': {'Polpo': 40, 'Gambero': 30, 'Verme': 30}, 'prede': ['Grongo', 'Spigola', 'Sarago', 'Triglia'], 'pastura': 'Pasturazione con polpo per fondo'},
    {'name': 'Peschici Scogliere', 'lat': 41.9500, 'lon': 16.0167, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Sardina', 'Cozza', 'Gamberetto'], 'percentuali': {'Sardina': 40, 'Cozza': 30, 'Gamberetto': 30}, 'prede': ['Sarago', 'Ombrina', 'Grongo', 'Cefalo'], 'pastura': 'Pasturazione con sardina per fondo'},
    {'name': 'Otranto Porto', 'lat': 40.1500, 'lon': 18.4833, 'techniques': ['Bolognese'], 'premium': False, 'esche': ['Verme', 'Arenicola', 'Sardina'], 'percentuali': {'Verme': 40, 'Arenicola': 30, 'Sardina': 30}, 'prede': ['Orata', 'Sarago', 'Spigola', 'Mormora'], 'pastura': 'Pastura fine con bigattino per bolognese'},
    {'name': 'Polignano Scogliere', 'lat': 40.9667, 'lon': 17.2167, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Gambero', 'Polpo', 'Cozza'], 'percentuali': {'Gambero': 50, 'Polpo': 30, 'Cozza': 20}, 'prede': ['Grongo', 'Sarago', 'Ombrina', 'Sgombro'], 'pastura': 'Pasturazione con gambero per fondo'},
    {'name': 'Torre dell\'Orso Spiaggia', 'lat': 40.2667, 'lon': 18.4333, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Arenicola', 'Sardina', 'Verme'], 'percentuali': {'Arenicola': 40, 'Sardina': 30, 'Verme': 30}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Triglia'], 'pastura': 'Pastura con arenicola e sardina per lunghe distanze'},
    {'name': 'Taranto Golfo', 'lat': 40.4667, 'lon': 17.2333, 'techniques': ['Surfcasting', 'Spinning'], 'premium': False, 'esche': ['Cozza', 'Gambero', 'Polpo'], 'percentuali': {'Cozza': 40, 'Gambero': 30, 'Polpo': 30}, 'prede': ['Spigola', 'Orata', 'Sarago', 'Cefalo'], 'pastura': 'Pastura mista cozza e sardina'},
    {'name': 'Gallipoli Molo', 'lat': 40.0500, 'lon': 17.9833, 'techniques': ['Bolognese'], 'premium': False, 'esche': ['Verme', 'Sardina', 'Arenicola'], 'percentuali': {'Verme': 40, 'Sardina': 30, 'Arenicola': 30}, 'prede': ['Sarago', 'Orata', 'Grongo', 'Sgombro'], 'pastura': 'Pastura fine con bigattino per bolognese'},
    {'name': 'Leuca Punta', 'lat': 39.8000, 'lon': 18.3500, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Spinning'], 'premium': True, 'esche': ['Gambero', 'Cozza', 'Verme'], 'percentuali': {'Gambero': 50, 'Cozza': 30, 'Verme': 20}, 'prede': ['Spigola', 'Sarago', 'Ombrina', 'Triglia'], 'pastura': 'Pastura leggera con gambero per spinning'},
    {'name': 'Manfredonia Spiaggia', 'lat': 41.6333, 'lon': 15.9167, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Arenicola', 'Polpo', 'Sardina'], 'percentuali': {'Arenicola': 40, 'Polpo': 30, 'Sardina': 30}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Cefalo'], 'pastura': 'Pastura con arenicola e formaggio'},
    {'name': 'Barletta Litorale', 'lat': 41.3167, 'lon': 16.2833, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Cozza', 'Verme', 'Gambero'], 'percentuali': {'Cozza': 40, 'Verme': 30, 'Gambero': 30}, 'prede': ['Orata', 'Sarago', 'Spigola', 'Grongo'], 'pastura': 'Pastura mista cozza e sardina'},
    {'name': 'Monopoli Calette', 'lat': 40.9500, 'lon': 17.3000, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': True, 'esche': ['Sardina', 'Polpo', 'Arenicola'], 'percentuali': {'Sardina': 40, 'Polpo': 30, 'Arenicola': 30}, 'prede': ['Grongo', 'Ombrina', 'Sarago', 'Sgombro'], 'pastura': 'Pasturazione con sardina per fondo'},
    {'name': 'Brindisi Porto', 'lat': 40.6333, 'lon': 17.9333, 'techniques': ['Bolognese'], 'premium': True, 'esche': ['Gambero', 'Verme', 'Cozza'], 'percentuali': {'Gambero': 50, 'Verme': 30, 'Cozza': 20}, 'prede': ['Sarago', 'Spigola', 'Orata', 'Triglia'], 'pastura': 'Pastura fine con gambero per bolognese'},

    # Sicilia (11 spot)
    {'name': 'Taormina Bay', 'lat': 37.8500, 'lon': 15.2833, 'techniques': ['Spinning', 'Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Gambero', 'Sardina', 'Verme'], 'percentuali': {'Gambero': 40, 'Sardina': 30, 'Verme': 30}, 'prede': ['Spigola', 'Sarago', 'Orata', 'Sgombro'], 'pastura': 'Pastura leggera con gambero per spinning'},
    {'name': 'Sciacca Porto', 'lat': 37.5000, 'lon': 13.0833, 'techniques': ['Bolognese'], 'premium': False, 'esche': ['Cozza', 'Arenicola', 'Polpo'], 'percentuali': {'Cozza': 40, 'Arenicola': 30, 'Polpo': 30}, 'prede': ['Sarago', 'Orata', 'Grongo', 'Triglia'], 'pastura': 'Pastura fine con cozza per bolognese'},
    {'name': 'Lampedusa Cala Pulcino', 'lat': 35.5000, 'lon': 12.6000, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Verme', 'Gambero', 'Sardina'], 'percentuali': {'Verme': 40, 'Gambero': 30, 'Sardina': 30}, 'prede': ['Orata', 'Sarago', 'Ombrina', 'Cefalo'], 'pastura': 'Pasturazione con verme per fondo'},
    {'name': 'Favignana Egadi', 'lat': 37.9333, 'lon': 12.3167, 'techniques': ['Spinning'], 'premium': False, 'esche': ['Sardina', 'Gamberetto', 'Polpo'], 'percentuali': {'Sardina': 50, 'Gamberetto': 30, 'Polpo': 20}, 'prede': ['Spigola', 'Grongo', 'Sarago', 'Sgombro'], 'pastura': 'Pastura minima – spinning puro'},
    {'name': 'Capo Peloro', 'lat': 38.2667, 'lon': 15.6333, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Arenicola', 'Cozza', 'Verme'], 'percentuali': {'Arenicola': 40, 'Cozza': 30, 'Verme': 30}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Triglia'], 'pastura': 'Pastura con arenicola per lunghe distanze'},
    {'name': 'Catania Moli', 'lat': 37.5000, 'lon': 15.0833, 'techniques': ['Bolognese', 'Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Gambero', 'Sardina', 'Polpo'], 'percentuali': {'Gambero': 40, 'Sardina': 30, 'Polpo': 30}, 'prede': ['Sarago', 'Grongo', 'Spigola', 'Cefalo'], 'pastura': 'Pastura mista gambero e sardina'},
    {'name': 'Siracusa Porto', 'lat': 37.0667, 'lon': 15.2833, 'techniques': ['Spinning'], 'premium': True, 'esche': ['Verme', 'Gambero', 'Cozza'], 'percentuali': {'Verme': 40, 'Gambero': 30, 'Cozza': 30}, 'prede': ['Spigola', 'Sarago', 'Orata', 'Mormora'], 'pastura': 'Pastura minima – spinning puro'},
    {'name': 'Trapani Scogliere', 'lat': 38.0167, 'lon': 12.5167, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': True, 'esche': ['Polpo', 'Sardina', 'Arenicola'], 'percentuali': {'Polpo': 50, 'Sardina': 30, 'Arenicola': 20}, 'prede': ['Grongo', 'Ombrina', 'Sarago', 'Sgombro'], 'pastura': 'Pasturazione con polpo per fondo profondo'},
    {'name': 'Palermo Lungomare', 'lat': 38.1167, 'lon': 13.3667, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Cozza', 'Verme', 'Gambero'], 'percentuali': {'Cozza': 40, 'Verme': 30, 'Gambero': 30}, 'prede': ['Orata', 'Sarago', 'Spigola', 'Triglia'], 'pastura': 'Pastura con cozza e sardina per lunghe distanze'},
    {'name': 'Cefalù Spiaggia', 'lat': 38.0333, 'lon': 14.0167, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Arenicola', 'Sardina', 'Polpo'], 'percentuali': {'Arenicola': 40, 'Sardina': 30, 'Polpo': 30}, 'prede': ['Orata', 'Mormora', 'Sarago', 'Cefalo'], 'pastura': 'Pastura con arenicola e formaggio'},
    {'name': 'Messina Stretto', 'lat': 38.2000, 'lon': 15.5500, 'techniques': ['Spinning'], 'premium': True, 'esche': ['Gambero', 'Verme', 'Cozza'], 'percentuali': {'Gambero': 50, 'Verme': 30, 'Cozza': 20}, 'prede': ['Spigola', 'Sarago', 'Grongo', 'Sgombro'], 'pastura': 'Pastura minima – spinning puro'},

    # Sardegna (11 spot)
    {'name': 'Alghero Litorale', 'lat': 40.5667, 'lon': 8.3167, 'techniques': ['Surfcasting', 'Spinning'], 'premium': False, 'esche': ['Arenicola', 'Gambero', 'Sardina'], 'percentuali': {'Arenicola': 40, 'Gambero': 30, 'Sardina': 30}, 'prede': ['Orata', 'Spigola', 'Sarago', 'Cefalo'], 'pastura': 'Pastura con arenicola e sardina per surfcasting'},
    {'name': 'Stintino Spiaggia', 'lat': 40.9333, 'lon': 8.2333, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Cozza', 'Verme', 'Arenicola'], 'percentuali': {'Cozza': 45, 'Verme': 35, 'Arenicola': 20}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Triglia'], 'pastura': 'Pastura con cozza e formaggio per lunghe distanze'},
    {'name': 'Capo Falcone', 'lat': 41.0000, 'lon': 8.4000, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Polpo', 'Sardina', 'Gambero'], 'percentuali': {'Polpo': 40, 'Sardina': 30, 'Gambero': 30}, 'prede': ['Grongo', 'Ombrina', 'Sarago', 'Sgombro'], 'pastura': 'Pasturazione con polpo per fondo profondo'},
    {'name': 'Golfo Aranci Spiaggia Bianca', 'lat': 40.9833, 'lon': 9.6167, 'techniques': ['Surfcasting', 'Bolognese'], 'premium': False, 'esche': ['Verme', 'Cozza', 'Gamberetto'], 'percentuali': {'Verme': 40, 'Cozza': 30, 'Gamberetto': 30}, 'prede': ['Sarago', 'Orata', 'Spigola', 'Cefalo'], 'pastura': 'Pastura fine con bigattino per bolognese'},
    {'name': 'Villasimius Capo Carbonara', 'lat': 39.1167, 'lon': 9.5167, 'techniques': ['Spinning'], 'premium': False, 'esche': ['Gambero', 'Sardina', 'Verme'], 'percentuali': {'Gambero': 50, 'Sardina': 30, 'Verme': 20}, 'prede': ['Spigola', 'Sarago', 'Grongo', 'Triglia'], 'pastura': 'Pastura minima – spinning puro'},
    {'name': 'Cagliari Poetto', 'lat': 39.2000, 'lon': 9.1500, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Arenicola', 'Cozza', 'Polpo'], 'percentuali': {'Arenicola': 40, 'Cozza': 30, 'Polpo': 30}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Cefalo'], 'pastura': 'Pastura con arenicola e sardina per lunghe distanze'},
    {'name': 'Badesi Spiaggia', 'lat': 40.9667, 'lon': 8.8833, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Sardina', 'Gambero', 'Verme'], 'percentuali': {'Sardina': 40, 'Gambero': 30, 'Verme': 30}, 'prede': ['Orata', 'Spigola', 'Sarago', 'Mormora'], 'pastura': 'Pastura densa con sardina e formaggio'},
    {'name': 'Capo Caccia Scogliere', 'lat': 40.5667, 'lon': 8.1667, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': True, 'esche': ['Polpo', 'Cozza', 'Arenicola'], 'percentuali': {'Polpo': 50, 'Cozza': 30, 'Arenicola': 20}, 'prede': ['Grongo', 'Ombrina', 'Sarago', 'Sgombro'], 'pastura': 'Pasturazione con polpo per fondo profondo'},
    {'name': 'Olbia Porto', 'lat': 40.9167, 'lon': 9.5000, 'techniques': ['Bolognese'], 'premium': True, 'esche': ['Verme', 'Gambero', 'Sardina'], 'percentuali': {'Verme': 40, 'Gambero': 30, 'Sardina': 30}, 'prede': ['Sarago', 'Orata', 'Spigola', 'Cefalo'], 'pastura': 'Pastura fine con bigattino per bolognese'},
    {'name': 'La Maddalena Arcipelago', 'lat': 41.2167, 'lon': 9.4000, 'techniques': ['Spinning', 'Pesca a fondo dagli scogli/porto'], 'premium': True, 'esche': ['Gamberetto', 'Polpo', 'Cozza'], 'percentuali': {'Gamberetto': 40, 'Polpo': 30, 'Cozza': 30}, 'prede': ['Spigola', 'Sarago', 'Grongo', 'Triglia'], 'pastura': 'Pastura leggera con gamberetto per spinning'},
    {'name': 'Chia Spiaggia', 'lat': 38.8833, 'lon': 8.8833, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Arenicola', 'Sardina', 'Verme'], 'percentuali': {'Arenicola': 40, 'Sardina': 30, 'Verme': 30}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Cefalo'], 'pastura': 'Pastura con arenicola e formaggio'},

    # Emilia-Romagna / Veneto (11 spot)
    {'name': 'Cesenatico Molo', 'lat': 44.2000, 'lon': 12.4000, 'techniques': ['Bolognese', 'Spinning'], 'premium': False, 'esche': ['Verme', 'Gambero', 'Cozza'], 'percentuali': {'Verme': 40, 'Gambero': 30, 'Cozza': 30}, 'prede': ['Sarago', 'Orata', 'Spigola', 'Cefalo'], 'pastura': 'Pastura fine con bigattino per bolognese'},
    {'name': 'Cervia Spiaggia', 'lat': 44.2667, 'lon': 12.3500, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Arenicola', 'Sardina', 'Polpo'], 'percentuali': {'Arenicola': 40, 'Sardina': 30, 'Polpo': 30}, 'prede': ['Orata', 'Mormora', 'Sarago', 'Triglia'], 'pastura': 'Pastura con arenicola e sardina per lunghe distanze'},
    {'name': 'Rimini Diga', 'lat': 44.0667, 'lon': 12.5667, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Cozza', 'Verme', 'Gambero'], 'percentuali': {'Cozza': 40, 'Verme': 30, 'Gambero': 30}, 'prede': ['Spigola', 'Orata', 'Sarago', 'Cefalo'], 'pastura': 'Pastura mista cozza e sardina'},
    {'name': 'Lignano Riviera', 'lat': 45.6833, 'lon': 13.1167, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Sardina', 'Arenicola', 'Polpo'], 'percentuali': {'Sardina': 40, 'Arenicola': 30, 'Polpo': 30}, 'prede': ['Orata', 'Spigola', 'Mormora', 'Cefalo'], 'pastura': 'Pastura con sardina e formaggio'},
    {'name': 'Chioggia Laguna', 'lat': 45.2167, 'lon': 12.2833, 'techniques': ['Bolognese'], 'premium': False, 'esche': ['Gambero', 'Verme', 'Cozza'], 'percentuali': {'Gambero': 50, 'Verme': 30, 'Cozza': 20}, 'prede': ['Sarago', 'Orata', 'Spigola', 'Mormora'], 'pastura': 'Pastura fine con gambero per bolognese'},
    {'name': 'Bellaria Spiaggia', 'lat': 44.1333, 'lon': 12.4667, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Arenicola', 'Sardina', 'Gambero'], 'percentuali': {'Arenicola': 40, 'Sardina': 30, 'Gambero': 30}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Triglia'], 'pastura': 'Pastura con arenicola e sardina per lunghe distanze'},
    {'name': 'Marina di Ravenna Diga', 'lat': 44.4833, 'lon': 12.2833, 'techniques': ['Spinning'], 'premium': True, 'esche': ['Verme', 'Polpo', 'Cozza'], 'percentuali': {'Verme': 40, 'Polpo': 30, 'Cozza': 30}, 'prede': ['Spigola', 'Sarago', 'Grongo', 'Sgombro'], 'pastura': 'Pastura minima – spinning puro'},
    {'name': 'Porto Garibaldi', 'lat': 44.6833, 'lon': 12.2333, 'techniques': ['Bolognese'], 'premium': True, 'esche': ['Gambero', 'Sardina', 'Verme'], 'percentuali': {'Gambero': 40, 'Sardina': 30, 'Verme': 30}, 'prede': ['Sarago', 'Orata', 'Spigola', 'Cefalo'], 'pastura': 'Pastura fine con gambero per bolognese'},
    {'name': 'Comacchio Canali', 'lat': 44.7000, 'lon': 12.1833, 'techniques': ['Spinning'], 'premium': True, 'esche': ['Cozza', 'Polpo', 'Arenicola'], 'percentuali': {'Cozza': 50, 'Polpo': 30, 'Arenicola': 20}, 'prede': ['Spigola', 'Grongo', 'Sarago', 'Triglia'], 'pastura': 'Pastura minima – spinning puro'},
    {'name': 'Caorle Spiaggia', 'lat': 45.6000, 'lon': 12.8833, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Sardina', 'Gambero', 'Verme'], 'percentuali': {'Sardina': 40, 'Gambero': 30, 'Verme': 30}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Cefalo'], 'pastura': 'Pastura con sardina e formaggio'},
    {'name': 'Jesolo Lido', 'lat': 45.5167, 'lon': 12.6667, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Arenicola', 'Cozza', 'Polpo'], 'percentuali': {'Arenicola': 40, 'Cozza': 30, 'Polpo': 30}, 'prede': ['Orata', 'Sarago', 'Spigola', 'Triglia'], 'pastura': 'Pastura con arenicola e sardina'},

    # Calabria (10 spot)
    {'name': 'Tropea Scogliere', 'lat': 38.6833, 'lon': 15.9000, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Spinning'], 'premium': False, 'esche': ['Polpo', 'Gambero', 'Verme'], 'percentuali': {'Polpo': 40, 'Gambero': 30, 'Verme': 30}, 'prede': ['Grongo', 'Spigola', 'Sarago', 'Triglia'], 'pastura': 'Pasturazione con polpo per fondo'},
    {'name': 'Diamante Spiaggia', 'lat': 39.6833, 'lon': 15.8167, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Arenicola', 'Sardina', 'Cozza'], 'percentuali': {'Arenicola': 40, 'Sardina': 30, 'Cozza': 30}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Cefalo'], 'pastura': 'Pastura con arenicola e sardina per lunghe distanze'},
    {'name': 'Scilla Stretto', 'lat': 38.2500, 'lon': 15.7167, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Verme', 'Polpo', 'Gambero'], 'percentuali': {'Verme': 50, 'Polpo': 30, 'Gambero': 20}, 'prede': ['Grongo', 'Sarago', 'Ombrina', 'Sgombro'], 'pastura': 'Pasturazione con polpo per fondo profondo'},
    {'name': 'Reggio Calabria Lungomare', 'lat': 38.1167, 'lon': 15.6500, 'techniques': ['Spinning', 'Bolognese'], 'premium': False, 'esche': ['Sardina', 'Cozza', 'Verme'], 'percentuali': {'Sardina': 40, 'Cozza': 30, 'Verme': 30}, 'prede': ['Spigola', 'Sarago', 'Orata', 'Cefalo'], 'pastura': 'Pastura fine con sardina per bolognese'},
    {'name': 'Capo Vaticano', 'lat': 38.6167, 'lon': 15.8333, 'techniques': ['Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Gambero', 'Arenicola', 'Polpo'], 'percentuali': {'Gambero': 40, 'Arenicola': 30, 'Polpo': 30}, 'prede': ['Grongo', 'Ombrina', 'Spigola', 'Sarago'], 'pastura': 'Pasturazione con gambero per fondo'},
    {'name': 'Crotone Porto', 'lat': 39.0833, 'lon': 17.1333, 'techniques': ['Bolognese'], 'premium': True, 'esche': ['Verme', 'Sardina', 'Cozza'], 'percentuali': {'Verme': 40, 'Sardina': 30, 'Cozza': 30}, 'prede': ['Sarago', 'Orata', 'Spigola', 'Mormora'], 'pastura': 'Pastura fine con bigattino per bolognese'},
    {'name': 'Soverato Spiaggia', 'lat': 38.6833, 'lon': 16.5500, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Arenicola', 'Gambero', 'Polpo'], 'percentuali': {'Arenicola': 40, 'Gambero': 30, 'Polpo': 30}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Triglia'], 'pastura': 'Pastura con arenicola e formaggio'},
    {'name': 'Roccella Ionica', 'lat': 38.3167, 'lon': 16.4000, 'techniques': ['Spinning'], 'premium': True, 'esche': ['Sardina', 'Verme', 'Cozza'], 'percentuali': {'Sardina': 50, 'Verme': 30, 'Cozza': 20}, 'prede': ['Spigola', 'Sarago', 'Grongo', 'Sgombro'], 'pastura': 'Pastura minima – spinning puro'},
    {'name': 'Cosenza Costa', 'lat': 39.3000, 'lon': 16.2500, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Gambero', 'Polpo', 'Arenicola'], 'percentuali': {'Gambero': 40, 'Polpo': 30, 'Arenicola': 30}, 'prede': ['Orata', 'Spigola', 'Sarago', 'Cefalo'], 'pastura': 'Pastura con gambero e sardina'},
    {'name': 'Vibo Marina', 'lat': 38.7167, 'lon': 16.1167, 'techniques': ['Bolognese'], 'premium': True, 'esche': ['Cozza', 'Verme', 'Sardina'], 'percentuali': {'Cozza': 40, 'Verme': 30, 'Sardina': 30}, 'prede': ['Sarago', 'Orata', 'Grongo', 'Triglia'], 'pastura': 'Pastura fine con cozza per bolognese'},

    # Abruzzo (5 spot)
    {'name': 'Pescara Molo Nord', 'lat': 42.4694, 'lon': 14.2156, 'techniques': ['Bolognese', 'Spinning'], 'premium': False, 'esche': ['Verme', 'Gambero', 'Sardina'], 'percentuali': {'Verme': 40, 'Gambero': 35, 'Sardina': 25}, 'prede': ['Spigola', 'Sarago', 'Orata', 'Cefalo'], 'pastura': 'Pastura fine con bigattino per bolognese'},
    {'name': 'Ortona Porto', 'lat': 42.3567, 'lon': 14.4067, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Bolognese'], 'premium': False, 'esche': ['Cozza', 'Polpo', 'Arenicola'], 'percentuali': {'Cozza': 45, 'Polpo': 30, 'Arenicola': 25}, 'prede': ['Grongo', 'Sarago', 'Ombrina', 'Triglia'], 'pastura': 'Pasturazione con polpo per fondo'},
    {'name': 'Vasto Punta Penna', 'lat': 42.1667, 'lon': 14.7167, 'techniques': ['Surfcasting', 'Spinning'], 'premium': False, 'esche': ['Sardina', 'Verme', 'Gambero'], 'percentuali': {'Sardina': 40, 'Verme': 30, 'Gambero': 30}, 'prede': ['Orata', 'Spigola', 'Mormora', 'Cefalo'], 'pastura': 'Pastura con sardina per lunghe distanze'},
    {'name': 'Torre Cerrano (Pineto)', 'lat': 42.5833, 'lon': 14.1000, 'techniques': ['Surfcasting'], 'premium': True, 'esche': ['Arenicola', 'Cozza', 'Polpo'], 'percentuali': {'Arenicola': 45, 'Cozza': 30, 'Polpo': 25}, 'prede': ['Orata', 'Sarago', 'Spigola', 'Triglia'], 'pastura': 'Pastura con arenicola e formaggio'},
    {'name': 'Fossacesia Marina Scogli', 'lat': 42.2333, 'lon': 14.5000, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Spinning'], 'premium': True, 'esche': ['Gambero', 'Sardina', 'Verme'], 'percentuali': {'Gambero': 50, 'Sardina': 30, 'Verme': 20}, 'prede': ['Grongo', 'Ombrina', 'Sarago', 'Sgombro'], 'pastura': 'Pastura leggera con gambero per spinning'},

    # Marche (5 spot)
    {'name': 'Ancona Porto Antico', 'lat': 43.6200, 'lon': 13.5100, 'techniques': ['Bolognese', 'Spinning'], 'premium': False, 'esche': ['Verme', 'Gambero', 'Cozza'], 'percentuali': {'Verme': 40, 'Gambero': 35, 'Cozza': 25}, 'prede': ['Sarago', 'Orata', 'Spigola', 'Cefalo'], 'pastura': 'Pastura fine con bigattino per bolognese'},
    {'name': 'Senigallia Spiaggia di Velluto', 'lat': 43.7167, 'lon': 13.2167, 'techniques': ['Surfcasting'], 'premium': False, 'esche': ['Arenicola', 'Sardina', 'Polpo'], 'percentuali': {'Arenicola': 45, 'Sardina': 30, 'Polpo': 25}, 'prede': ['Orata', 'Mormora', 'Spigola', 'Triglia'], 'pastura': 'Pastura con arenicola e sardina per lunghe distanze'},
    {'name': 'Fano Molo', 'lat': 43.8500, 'lon': 13.0167, 'techniques': ['Bolognese', 'Pesca a fondo dagli scogli/porto'], 'premium': False, 'esche': ['Cozza', 'Verme', 'Gambero'], 'percentuali': {'Cozza': 40, 'Verme': 35, 'Gambero': 25}, 'prede': ['Spigola', 'Sarago', 'Grongo', 'Mormora'], 'pastura': 'Pastura mista cozza e sardina'},
    {'name': 'Numana Riviera del Conero', 'lat': 43.5167, 'lon': 13.6167, 'techniques': ['Pesca a fondo dagli scogli/porto', 'Spinning'], 'premium': True, 'esche': ['Polpo', 'Sardina', 'Arenicola'], 'percentuali': {'Polpo': 50, 'Sardina': 30, 'Arenicola': 20}, 'prede': ['Grongo', 'Ombrina', 'Sarago', 'Sgombro'], 'pastura': 'Pasturazione con polpo per fondo profondo'},
    {'name': 'Grottammare Lungomare Sud', 'lat': 42.9833, 'lon': 13.8667, 'techniques': ['Surfcasting', 'Spinning'], 'premium': True, 'esche': ['Gambero', 'Verme', 'Cozza'], 'percentuali': {'Gambero': 45, 'Verme': 35, 'Cozza': 20}, 'prede': ['Orata', 'Spigola', 'Sarago', 'Triglia'], 'pastura': 'Pastura densa con gambero e sardina'}
]

# ------------------------------- FUNZIONI DATI -------------------------------
def fetch_meteo(lat, lon):
    return {
        'wind_dir': random.choice(['N', 'S', 'E', 'O', 'NE', 'SE', 'NO', 'SO']),
        'wind_speed': round(random.uniform(5, 20), 1),
        'wave_height': round(random.uniform(0.5, 1.5), 1),
        'rain_prob': random.randint(0, 30),
        'pressure': random.randint(1000, 1025),
        'water_temp': random.randint(14, 18)
    }

def fetch_tides(spot_name):
    seed = int(hashlib.md5(spot_name.encode()).hexdigest(), 16) % 100
    low_hour = 6 + (seed % 6)
    high_hour = low_hour + 6
    if high_hour > 23:
        high_hour -= 12
    return {
        'low': f"{low_hour:02d}:00",
        'high': f"{high_hour:02d}:00",
        'coeff': 50 + (seed % 50)
    }

def calculate_solunar(spot_name, selected_date):
    seed = int(hashlib.md5((str(selected_date) + spot_name).encode()).hexdigest(), 16) % 100
    peak = 60 + (seed % 36)
    hour = 6 + (seed % 12)
    return {
        'peak': peak,
        'time': f"{hour:02d}:00-{hour+3:02d}:00",
        'moon_phase': random.choice(['Calante', 'Crescente', 'Piena', 'Nuova'])
    }

def calculate_rating(meteo, tides, solunar, spot_name, selected_date):
    seed_str = str(selected_date) + spot_name
    seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % 1000000
    random.seed(seed)
    
    score = 100
    if meteo['wind_speed'] > 10: score -= 10
    if meteo['wind_speed'] > 15: score -= 20
    if meteo['wave_height'] > 0.8: score -= 10
    if meteo['wave_height'] > 1.2: score -= 15
    if tides['coeff'] < 70: score -= 10
    if tides['coeff'] < 50: score -= 20
    if solunar['peak'] < 80: score -= 10
    if solunar['peak'] < 70: score -= 15
    score += random.randint(-10, 10)
    return max(0, min(100, score))

def get_color(rating):
    if rating <= 50: return [255, 255, 255, 200]
    if rating <= 70: return [255, 255, 0, 200]
    if rating <= 89: return [255, 165, 0, 200]
    return [255, 0, 0, 200]

# -------------------------------- GENERA REPORT -------------------------------
def generate_fishing_info(spot, selected_date, is_premium):
    meteo = fetch_meteo(spot['lat'], spot['lon'])
    tides = fetch_tides(spot['name'])
    solunar = calculate_solunar(spot['name'], selected_date)
    rating = calculate_rating(meteo, tides, solunar, spot['name'], selected_date)

    # Orario arrivo variabile (1h prima picco solunare)
    peak_start = int(solunar['time'].split('-')[0].split(':')[0])
    arrival_hour = peak_start - 1 if peak_start > 1 else 23
    arrival = f"{arrival_hour:02d}:30"

    info = f"""
**1. Valutazione giornata ({rating}/100) + Marea + Meteo**  
Valutazione: {"Eccellente" if rating > 89 else "Buona" if rating > 70 else "Media" if rating > 50 else "Bassa"}.  
Marea: Bassa {tides['low']}, Alta {tides['high']}, coefficiente {tides['coeff']}.  
Meteo: Vento {meteo['wind_dir']} {meteo['wind_speed']} nodi, onda {meteo['wave_height']}m, pioggia {meteo['rain_prob']}%, pressione {meteo['pressure']} hPa, temp acqua {meteo['water_temp']}°C.
    """

    if is_premium:
        info += f"""
**Solunare dettagliato**  
Picco attività {solunar['peak']}% nella fascia {solunar['time']}, fase luna {solunar['moon_phase']}.
        """

    info += f"""
**2. Descrizione dello spot**  
Coordinate: {spot['lat']:.6f}°N {spot['lon']:.6f}°E → [Apri in Google Maps](https://www.google.com/maps?q={spot['lat']},{spot['lon']})  
Fondale misto sabbia/scogli, profondità 3-15m a lancio, correnti moderate.
    """

    info += f"""
**3. Tecnica consigliata**  
Primaria: {spot['techniques'][0]}  
{"Montatura completa: canna 4.2m, mulinello 5000, filo 0.25mm. Trucchi per buche." if is_premium else ""}
    """

    info += f"""
**4. Esche consigliate + prede possibili + pastura**  
1. {spot['esche'][0]} {"(" + str(spot['percentuali'][spot['esche'][0]]) + "%)" if is_premium else ""}  
2. {spot['esche'][1]} {"(" + str(spot['percentuali'][spot['esche'][1]]) + "%)" if is_premium else ""}  
3. {spot['esche'][2]} {"(" + str(spot['percentuali'][spot['esche'][2]]) + "%)" if is_premium else ""}  
Prede principali: {', '.join(spot['prede'])}  
Pastura consigliata: {spot['pastura']}
    """

    info += f"""
**5. Programma di pesca completo**  
Orario di arrivo consigliato: {arrival} (1h prima picco solunare)  
Fase 1: Setup e pasturazione  
Fase 2: Primi lanci all'alba o tramonto  
Fase 3: Picco attività {solunar['time']} – controlli frequenti  
Fase 4: Pesca fino al calare del sole o chiusura notturna  
Chiusura sessione: entro le 22:00 o alba successiva
    """

    if is_premium:
        info += """
**Extra Premium**  
- Montature dettagliate e trucchi locali  
- Note personali salvabili  
- Galleria catture community  
- Segnala rifiuti a Legambiente → 1 settimana gratis!
        """

    return info

# -------------------------------- MAPPA E CALCOLI -----------------------------
visible_spots = [s for s in spots if is_premium or not s.get('premium', False)]

filtered_spots = [
    s for s in visible_spots
    if technique == "Tutte" or technique in s['techniques']
]

spot_data = []
for spot in filtered_spots:
    meteo = fetch_meteo(spot['lat'], spot['lon'])
    tides = fetch_tides(spot['name'])
    solunar = calculate_solunar(spot['name'], selected_date)
    rating = calculate_rating(meteo, tides, solunar, spot['name'], selected_date)
    spot_data.append({
        'name': spot['name'],
        'lat': spot['lat'],
        'lon': spot['lon'],
        'rating': rating,
        'color': get_color(rating),
        'meteo': meteo,
        'tides': tides,
        'solunar': solunar
    })

df_spots = pd.DataFrame(spot_data)

if not df_spots.empty:
    layer = pdk.Layer(
        "ScatterplotLayer",
        df_spots,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=6,
        radius_max_pixels=20,
        get_position="[lon, lat]",
        get_radius=50,
        get_fill_color="color",
        get_line_color=[0, 0, 0],
    )

    tooltip = {"html": "<b>{name}</b><br>Valutazione: {rating}/100", "style": {"background": "grey", "color": "white"}}

    view_state = pdk.ViewState(latitude=41.9, longitude=12.5, zoom=5, pitch=0)

    deck = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
    st.pydeck_chart(deck, use_container_width=True)
else:
    st.info("Nessuno spot disponibile con i filtri selezionati.")

# -------------------------------- REPORT -------------------------------------
if not df_spots.empty:
    selected_name = st.selectbox("Seleziona spot per report completo", df_spots['name'].tolist())

    if selected_name:
        selected = df_spots[df_spots['name'] == selected_name].iloc[0]
        spot = next(s for s in filtered_spots if s['name'] == selected_name)
        st.subheader(f"Report: {selected_name} – {selected_date.strftime('%d %B %Y')}")

        report = generate_fishing_info(spot, selected_date, is_premium)
        st.markdown(report)

st.markdown("***Messaggio green:*** Porta via i tuoi rifiuti e, se puoi, anche quelli altrui. Un vero pescatore protegge il suo spot 🌿")
st.caption("RivaPro – Pesca da Riva Responsabile 🇮🇹 | Versione aggiornata 2026")
