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

def lag_klikkelyd():
    lyd = Sine(1000).to_audio_segment(duration=50).apply_gain(-3)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        lyd.export(f.name, format="wav")
        return f.name

lydfil = lag_klikkelyd()

if 'stopp' not in st.session_state:
    st.session_state.stopp = False

def spill_metronom(bpm, takter=8, slag_per_takt=4):
    intervall = 60 / bpm
    total_slag = takter * slag_per_takt
    for slag in range(total_slag):
        if st.session_state.stopp:
            break
        st.audio(lydfil, format="audio/wav", start_time=0)
        time.sleep(intervall)

def pause_nedtelling(sekunder=20):
    with st.empty():
        for i in range(sekunder, 0, -1):
            st.markdown(f"⏸️ Pause i {i} sekunder...")
            st.progress((sekunder - i) / sekunder)
            time.sleep(1)
        st.markdown("🎵 Fortsetter!")

tempoprogram = [48, 58, 72, 84, 96, 108, 120]
takter_per_tempo = 8

if start:
    st.session_state.stopp = False
    spill_metronom(tempo)

if stop:
    st.session_state.stopp = True

if program_knapp:
    st.session_state.stopp = False
    for bpm in tempoprogram:
        if st.session_state.stopp:
            break
        st.markdown(f"## 🔁 Tempo: {bpm} BPM")
        spill_metronom(bpm, takter=takter_per_tempo)
        if st.session_state.stopp:
            break
        pause_nedtelling(20)
    st.markdown("✅ Ferdig med hele programmet.")
