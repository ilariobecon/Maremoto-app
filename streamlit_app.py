import streamlit as st
import pydeck as pdk
import pandas as pd
import random
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# ────────────────────────────────────────────────
# Dati spot di esempio (espandi con i tuoi ~140+)
# ────────────────────────────────────────────────
data = {
    'nome': [
        'Spiaggia di Framura', 'Riva Trigoso', 'Follonica', 'Puntone',
        'Torvaianica', 'Molo Neroniano Anzio', 'Porto Acquamorta',
        'Porto Salerno Molo Manfredi', 'Lido Marini', 'Porto Cesareo',
        'Riva Ligure Milazzo', 'Torre Faro', 'Ostia Lido (Roma)',
        'Fiumicino (Roma)', 'Santa Marinella', 'Civitavecchia'
    ],
    'lat': [44.210, 44.270, 42.920, 42.900, 41.620, 41.450, 40.800, 40.680, 39.830, 40.260, 38.220, 38.260, 41.740, 41.730, 42.080, 42.090],
    'lon': [9.550, 9.410, 10.760, 10.780, 12.450, 12.630, 14.050, 14.750, 18.140, 17.890, 15.240, 15.630, 12.320, 12.240, 11.830, 11.790],
    'techniques': [
        ['spinning', 'bolognese'], ['surfcasting', 'pesca a fondo dagli scogli/porto'],
        ['bolognese', 'spinning'], ['surfcasting', 'pesca a fondo dagli scogli/porto'],
        ['surfcasting'], ['pesca a fondo dagli scogli/porto', 'spinning'],
        ['spinning', 'bolognese'], ['pesca a fondo dagli scogli/porto', 'surfcasting'],
        ['bolognese', 'spinning'], ['surfcasting'],
        ['spinning', 'pesca a fondo dagli scogli/porto'], ['surfcasting'],
        ['surfcasting', 'bolognese'], ['spinning', 'pesca a fondo dagli scogli/porto'],
        ['bolognese'], ['surfcasting']
    ],
    'premium': [False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True],
    'esche': [['verme', 'gambero', 'silicone'], ['calamaro', 'sarda', 'artificiale'], ['verme', 'mais', 'silicone'], ['gambero', 'seppia', 'artificiale'],
              ['verme', 'sarda'], ['calamaro', 'gambero'], ['silicone', 'gambero'], ['sarda', 'verme'], ['mais', 'verme'], ['gambero', 'seppia'],
              ['silicone', 'calamaro'], ['verme', 'sarda'], ['verme', 'mais'], ['silicone', 'calamaro'], ['mais', 'verme'], ['sarda', 'gambero']],
    'percentuali': [{'verme':60}, {'calamaro':75, 'sarda':50}, {'verme':55}, {'gambero':80, 'seppia':65}, {'verme':50}, {'calamaro':70},
                    {'silicone':60}, {'sarda':75}, {'mais':50}, {'gambero':65}, {'silicone':55}, {'verme':70}, {'verme':45}, {'silicone':65}, {'mais':55}, {'sarda':70}],
    'prede': [['spigola', 'orata'], ['serra', 'barracuda'], ['cefali', 'mormore'], ['saraghi', 'dentici'], ['orata', 'spigola'], ['seppie', 'calamari'],
              ['barracuda', 'serra'], ['spigola', 'dentici'], ['cefali', 'orata'], ['trigle', 'saraghi'], ['serra', 'spigola'], ['orata', 'barracuda'],
              ['orata', 'spigola'], ['serra', 'barracuda'], ['cefali', 'mormore'], ['dentici', 'saraghi']],
    'pastura': ['mais', 'sardine', 'pane', 'vermi', 'mais', 'sardine', 'artificiale', 'vermi', 'pane', 'mais', 'artificiale', 'sardine', 'mais', 'calamaro', 'pane', 'sardine'],
    'fondale': ['sabbioso', 'misto', 'sabbioso', 'roccioso', 'sabbioso', 'misto', 'roccioso', 'misto', 'sabbioso', 'misto', 'roccioso', 'sabbioso', 'sabbioso', 'roccioso', 'misto', 'sabbioso'],
    'profondita': ['2-5m', '5-10m', '2-5m', '10-15m', '5-10m', '5-10m', '5-10m', '10-15m', '2-5m', '5-10m', '5-10m', '2-5m', '2-5m', '5-10m', '2-5m', '5-10m'],
    'difficolta': ['semplice', 'difficile', 'intermedio', 'difficile', 'semplice', 'intermedio', 'intermedio', 'difficile', 'semplice', 'intermedio', 'intermedio', 'difficile', 'semplice', 'intermedio', 'semplice', 'difficile'],
    'tecnica_primaria': ['spinning', 'surfcasting', 'bolognese', 'pesca a fondo dagli scogli/porto', 'surfcasting', 'pesca a fondo dagli scogli/porto',
                         'spinning', 'pesca a fondo dagli scogli/porto', 'bolognese', 'surfcasting', 'spinning', 'surfcasting',
                         'surfcasting', 'spinning', 'bolognese', 'surfcasting']
}

df_spots = pd.DataFrame(data)

# Descrizioni personalizzate per tecnica
descrizioni_per_tecnica = {
    'surfcasting': "Ideale per lanci lunghi su fondali sabbiosi. Stagione top: autunno-inverno per spigole/orate. Prede target: orate, spigole. Nota: attenzione a correnti forti.",
    'pesca a fondo dagli scogli/porto': "Perfetta per spot rocciosi/portuali. Stagione: primavera-estate per saraghi/cefali. Prede: saraghi, triglie. Usa montature anti-incaglio.",
    'bolognese': "Adatta a acque calme, profondità medie. Stagione: tutto l'anno, picco estate. Prede: cefali, mormore. Flotta con precisione.",
    'spinning': "Dinamica per predatori. Stagione: estate-autunno. Prede: serra, spigole. Muoviti lungo la riva."
}

# Calcolo rating consistente
@st.cache_data
def calcola_rating(spot_name, data_str, tecnica_selezionata, tecnica_primaria):
    random.seed(hash(spot_name + data_str))
    base = random.randint(20, 100)
    if tecnica_selezionata == tecnica_primaria or tecnica_selezionata == 'Tutte':
        base += 15
    return min(base, 100)

def get_color(rating):
    if rating < 25: return [255, 255, 255, 160]      # bianco
    elif rating < 50: return [255, 255, 0, 160]      # giallo
    elif rating < 75: return [255, 165, 0, 160]      # arancione
    else: return [255, 0, 0, 160]                    # rosso

# ────────────────────────────────────────────────
# Interfaccia
# ────────────────────────────────────────────────
st.title("RivaPro – Pesca da Riva Responsabile in Italia")

# Sidebar
data = st.sidebar.date_input("Data", datetime.today())
tecnica = st.sidebar.selectbox("Tecnica", ['Tutte', 'Surfcasting', 'Pesca a fondo dagli scogli/porto', 'Bolognese', 'Spinning'])
is_premium = st.sidebar.checkbox("Accesso Premium")

# Filtra
df_filtered = df_spots.copy()
if tecnica != 'Tutte':
    df_filtered = df_filtered[df_filtered['techniques'].apply(lambda x: tecnica in x)]
if not is_premium:
    df_filtered = df_filtered[~df_filtered['premium']]

# Rating
data_str = str(data)
df_filtered['rating'] = df_filtered.apply(
    lambda row: calcola_rating(row['nome'], data_str, tecnica, row['tecnica_primaria']), axis=1
)
df_filtered['color'] = df_filtered['rating'].apply(get_color)

# Mappa
if not df_filtered.empty:
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=df_filtered,
        get_position=['lon', 'lat'],
        get_color='color',
        get_radius=200,
        pickable=True
    )
    view_state = pdk.ViewState(latitude=42.0, longitude=12.0, zoom=5)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
else:
    st.info("Nessuno spot disponibile con questi filtri.")

# Report spot selezionato
selected_spot = st.selectbox("Seleziona Spot", df_filtered['nome'])
if selected_spot:
    spot = df_filtered[df_filtered['nome'] == selected_spot].iloc[0]
    rating = spot['rating']

    st.subheader(f"Report {selected_spot} – {data_str}")
    st.write(f"**Rating:** {rating}/100")

    # Descrizione personalizzata
    tp = spot['tecnica_primaria']
    desc = f"Coordinate: {spot['lat']}, {spot['lon']} | [GMaps](https://maps.google.com/?q={spot['lat']},{spot['lon']})  \nFondale: {spot['fondale']} | Profondità: {spot['profondita']} | Difficoltà: {spot['difficolta']}"
    desc += f"\n\n**Per {tp}:** {descrizioni_per_tecnica.get(tp, 'Generico.')}"
    st.write(desc)

    # Tecnica consigliata
    st.write(f"**Tecnica consigliata:** {tp}")
    if is_premium:
        st.write("Montatura / Trucchi premium: usa lenze leggere per evitare incagli.")

    # Esche & %
    st.write("**Esche consigliate:**", ", ".join(spot.get('esche', [])))
    if is_premium:
        perc = spot.get('percentuali', {})
        if perc:
            st.write("**Percentuali cattura:**")
            for e, p in perc.items():
                st.write(f"- {e}: {p}%")
        st.write(f"**Prede principali:** {', '.join(spot['prede'])}  \n**Pastura:** {spot['pastura']}")
    else:
        st.info("Percentuali e prede dettagliate solo con Premium.")

    # Programma
    random.seed(hash(selected_spot + data_str))
    ora = random.randint(1, 3)
    st.write(f"**Orario arrivo consigliato:** {ora}h prima del picco solunare")

    # PDF export
    def create_pdf():
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, f"Report RivaPro – {selected_spot}")
        c.drawString(100, 730, f"Data: {data_str} | Rating: {rating}/100")
        c.drawString(100, 700, desc)
        c.save()
        buffer.seek(0)
        return buffer

    st.download_button(
        label="Scarica Report PDF",
        data=create_pdf(),
        file_name=f"{selected_spot.replace(' ', '_')}_report.pdf",
        mime="application/pdf"
    )

# Shop Affiliate (esempio Amazon – sostituisci con i tuoi link reali)
st.subheader("Shop Eco Sostenibile")
st.write("Link affiliati – guadagni una commissione se acquisti da qui (zero costi per te).")

prodotti = [
    ("Ami biodegradabili set 10", "https://amzn.to/TUO_LINK_1"),
    ("Fili riciclabili 50m", "https://amzn.to/TUO_LINK_2"),
    ("Piombi tungsteno set 5", "https://amzn.to/TUO_LINK_3")
]

for nome, link in prodotti:
    st.markdown(f"**{nome}** → [Acquista su Amazon]({link})")

# Footer green
st.markdown("---")
st.caption("**Pesca Responsabile** – Rilascia ciò che non consumi. Usa solo gear eco. 🌍🎣")
