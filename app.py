import streamlit as st
import time
import base64

st.set_page_config(page_title="Metronom", layout="centered")
st.title("🎵 Enkel Metronom med Program")

# === Kontrollpanel ===
tempo = st.slider("Velg tempo (BPM)", 30, 240, 100)
start = st.button("Start metronom")
stop = st.button("Stopp")
program_knapp = st.button("Program")

# === Lyd ===
try:
    with open("dark_click.wav", "rb") as f:
        lyd_mørk = f.read()
    with open("light_click.wav", "rb") as f:
        lyd_lys = f.read()
except FileNotFoundError:
    st.error("❌ Fant ikke klikkelydene. Sørg for at 'dark_click.wav' og 'light_click.wav' finnes i mappa.")
    st.stop()

# === Tilstand ===
if 'stopp' not in st.session_state:
    st.session_state.stopp = False

# === Lydspiller uten visuell komponent ===
def spill_lyd(data):
    lyd_base64 = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <audio autoplay>
            <source src="data:audio/wav;base64,{lyd_base64}" type="audio/wav">
        </audio>
        """,
        unsafe_allow_html=True
    )

# === Nedtelling med fremdriftsindikator og feilsikring ===
def pause_nedtelling(sekunder=5, tekst="Starter om"):
    try:
        sekunder = int(sekunder)
    except Exception:
        st.error("🚨 pause_nedtelling() fikk en ugyldig verdi for sekunder.")
        return

    box = st.empty()
    progress = st.empty()
    for i in range(sekunder, 0, -1):
        box.markdown(f"⏳ {tekst} {i} sekunder...")
        progress.progress((sekunder - i) / sekunder)
        time.sleep(1)
    box.markdown("🎬 Fortsetter!")
    progress.empty()

# === Spiller metronomen ===
def spill_metronom(bpm, takter=8, slag_per_takt=4):
    intervall = 60 / bpm
    total_slag = takter * slag_per_takt
    for i in range(total_slag):
        if st.session_state.stopp:
            break
        if i % slag_per_takt == 0:
            spill_lyd(lyd_mørk)
        else:
            spill_lyd(lyd_lys)
        time.sleep(intervall)

# === Tempo-program ===
tempoprogram = [48, 58, 72, 84, 96, 108, 120]
takter_per_tempo = 8
tempo_info = st.empty()

# === Enkel manuell metronom ===
if start:
    st.session_state.stopp = False
    tempo_info.markdown(f"## 🎯 Tempo: {tempo} BPM")
    spill_metronom(tempo)

if stop:
    st.session_state.stopp = True

# === Program-knapp: tempotrening ===
if program_knapp:
    st.session_state.stopp = False

    # Første nedtelling før start
    pause_nedtelling(5, tekst="Start om")

    for i, bpm in enumerate(tempoprogram):
        if st.session_state.stopp:
            break

        tempo_info.m_
