import streamlit as st
import tempfile
import matplotlib.pyplot as plt
from audio_processor import AudioProcessor
import config

# Initialisation de l'AudioProcessor
processor = AudioProcessor(device=config.DEVICE)

st.set_page_config(page_title="Audio Noise Reduction", layout="wide")
st.title("🎤 Voice Isolation and Noise Reduction")

# Téléchargement du fichier audio
uploaded_file = st.file_uploader("1️⃣ Upload an audio file (MP3 or WAV)", type=["mp3", "wav"])

if uploaded_file:
    with st.spinner("Processing your audio file..."):
        # Sauvegarde temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_input:
            temp_input.write(uploaded_file.read())
            input_audio_path = temp_input.name
        
        # Chemin temporaire pour le fichier nettoyé
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_output:
            output_audio_path = temp_output.name

    st.write("2️⃣ **Cleaning Audio with Demucs**")
    with st.spinner("Cleaning audio..."):
        original_signal, cleaned_signal, sample_rate = processor.clean_audio(
            input_audio_path, output_audio_path, config.LOW_CUTOFF, config.HIGH_CUTOFF
        )
    st.success("Audio cleaned successfully!")

    # Lecture audio
    col1, col2 = st.columns(2)
    with col1:
        st.write("Original Audio")
        st.audio(uploaded_file, format="audio/mp3")
    with col2:
        st.write("Cleaned Audio")
        st.audio(output_audio_path, format="audio/wav")

    # Visualisation des signaux
    st.write("#### Signal Comparison")
    fig, ax = plt.subplots()
    ax.plot(original_signal[0], label="Original Signal", color='blue', alpha=0.5)
    ax.plot(cleaned_signal[0], label="Cleaned Signal", color='orange', alpha=0.7)
    ax.set_title("Original vs Cleaned Audio Signal")
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("Amplitude")
    ax.legend()
    st.pyplot(fig)

    # Téléchargement du fichier nettoyé
    with open(output_audio_path, "rb") as f:
        st.download_button(
            label="Download Cleaned Audio",
            data=f,
            file_name="cleaned_audio.wav",
            mime="audio/wav",
        )
else:
    st.info("Upload an audio file to start.")