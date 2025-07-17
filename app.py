import streamlit as st
import time
import base64

st.set_page_config(page_title="Metronom", layout="centered")
st.title("🎵 Enkel Metronom med Program")

# Tempojustering og knapper
tempo = st.slider("Velg tempo (BPM)", 30, 240, 100)
start = st.button("Start metronom")
stop = st.button("Stopp")
program_knapp = st.button("Program")

# Last inn klikkelydene
try:
    with open("dark_click.wav", "rb") as f:
        lyd_mørk = f.read()
    with open("light_click.wav", "rb") as f:
        lyd_lys = f.read()
except FileNotFoundError:
    st.error("❌ Fant ikke klikkelydene. Sørg for at 'dark_click.wav' og 'light_click.wav' ligger i mappen.")
    st.stop()

# Intern tilstand
if 'stopp' not in st.session_state:
    st.session_state.stopp = False

# Spiller lyd usynlig via HTML
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

# Nedtelling med fremdrift
def pause_nedtelling(sekunder=5, tekst="Starter om"):
    with st.empty():
        for i in range(sekunder, 0, -1):
            st.markdown(f"⏳ {tekst} {i} sekunder...")
            st.progress((sekunder - i) / sekunder)
            time.sleep(1)
        st.markdown("🎬 Fortsetter!")

# Spill metronom med riktig takt
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

# Definert program
tempoprogram = [48, 58, 72, 84, 96, 108, 120]
takter_per_tempo = 8

# Enkelt metronom
if start:
    st.session_state.stopp = False
    spill_metronom(tempo)

# Stopp
if stop:
    st.session_state.stopp = True

# Tempoprogram med pauser og nedtelling
if program_knapp:
    st.session_state.stopp = False
    pause_nedtelling(5)
    for bpm in tempoprogram:
        if st.session_state.stopp:
            break
        st.markdown(f"## 🔁 Tempo: {bpm} BPM")
        spill_metronom(bpm, takter=takter_per_tempo)
        if st.session_state.stopp:
            break
        pause_nedtelling(20, tekst="Pause i")
    st.markdown("✅ Programmet er ferdig.")
