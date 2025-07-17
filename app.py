import streamlit as st
import time
from pydub.generators import Sine
from pydub import AudioSegment
import tempfile

st.title("🎵 Metronom med program")

tempo = st.slider("Velg tempo (BPM)", 30, 240, 100)
start = st.button("Start metronom")
stop = st.button("Stopp")
program_knapp = st.button("Program")

# === Lag to klikkelyder ===
def lag_klikkelyd(frekvens=1000):
    lyd = Sine(frekvens).to_audio_segment(duration=50).apply_gain(-3)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        lyd.export(f.name, format="wav")
        return f.name

lyd_lys = lag_klikkelyd(1000)
lyd_mørk = lag_klikkelyd(700)

if 'stopp' not in st.session_state:
    st.session_state.stopp = False

# === Nedtelling med progressbar ===
def pause_nedtelling(sekunder=5):
    with st.empty():
        for i in range(sekunder, 0, -1):
            st.markdown(f"⏳ Starter om {i} sekunder...")
            st.progress((sekunder - i) / sekunder)
            time.sleep(1)
        st.markdown("🎬 Starter!")

# === Spiller en takt med forskjellig første slag ===
def spill_metronom(bpm, takter=8, slag_per_takt=4):
    intervall = 60 / bpm
    total_slag = takter * slag_per_takt
    for i in range(total_slag):
        if st.session_state.stopp:
            break
        if i % slag_per_takt == 0:
            st.audio(lyd_mørk, format="audio/wav", start_time=0)
        else:
            st.audio(lyd_lys, format="audio/wav", start_time=0)
        time.sleep(intervall)

# === Tempo-programmet med 5 sek start og 20 sek pause ===
tempoprogram = [48, 58, 72, 84, 96, 108, 120]
takter_per_tempo = 8

if start:
    st.session_state.stopp = False
    spill_metronom(tempo)

if stop:
    st.session_state.stopp = True

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
        pause_nedtelling(20)
    st.markdown("✅ Ferdig med hele programmet.")
