import streamlit as st
import time

st.set_page_config(page_title="Metronom", layout="centered")
st.title("🎵 Enkel Metronom med Program")

tempo = st.slider("Velg tempo (BPM)", 30, 240, 100)
start = st.button("Start metronom")
stop = st.button("Stopp")
program_knapp = st.button("Program")

# Last inn lydfilene
try:
    with open("dark_click.wav", "rb") as f:
        lyd_mørk = f.read()
    with open("light_click.wav", "rb") as f:
        lyd_lys = f.read()
except FileNotFoundError:
    st.error("❌ Fant ikke klikkelydene. Sørg for at 'dark_click.wav' og 'light_click.wav' finnes i mappa.")
    st.stop()

# Intern stoppstatus
if 'stopp' not in st.session_state:
    st.session_state.stopp = False

def pause_nedtelling(sekunder=5, tekst="Starter om"):
    with st.empty():
        for i in range(sekunder, 0, -1):
            st.markdown(f"⏳ {tekst} {i} sekunder...")
            st.progress((sekunder - i) / sekunder)
            time.sleep(1)
        st.markdown("🎬 Fortsetter!")

def spill_metronom(bpm, takter=8, slag_per_takt=4):
    intervall = 60 / bpm
    total_slag = takter * slag_per_takt
    for i in range(total_slag):
        if st.session_state.stopp:
            break
        if i % slag_per_takt == 0:
            st.audio(lyd_mørk, format="audio/wav")
        else:
            st.audio(lyd_lys, format="audio/wav")
        time.sleep(intervall)

# Fast program
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
        pause_nedtelling(20, tekst="Pause i")
    st.markdown("✅ Programmet er ferdig.")
