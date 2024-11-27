import streamlit as st
import tempfile
import matplotlib.pyplot as plt
from audio_processor import AudioProcessor
import config

# Initialize AudioProcessor with the appropriate device
processor = AudioProcessor(device=config.DEVICE)

# Configure the Streamlit page layout and title
st.set_page_config(page_title="Analyse Audio - Hetic Radio", layout="wide")
st.title("🎵 Analyse Audio - Fait par HeticSolutions pour Hetic Radio")

# Step 1: File upload
# Allow users to upload an MP3 or WAV file for analysis and cleaning
st.header("1️⃣ Téléversez un fichier audio")
st.write("""
    Bienvenue dans notre outil d'analyse audio. Téléversez un fichier au format MP3 ou WAV pour le 
    nettoyer et analyser sa qualité sonore.
""")
uploaded_file = st.file_uploader("Choisissez un fichier audio :", type=["mp3", "wav"])

if uploaded_file:
    st.info("🎤 Fichier audio téléversé avec succès !")

    # Save the uploaded file temporarily for processing
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_input:
        temp_input.write(uploaded_file.read())
        input_audio_path = temp_input.name

    # Save cleaned audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_output:
        output_audio_path = temp_output.name

    # Step 2: Clean the audio using the AudioProcessor
    st.subheader("2️⃣ Nettoyage de l'audio")
    st.write("""
        Nous utilisons des technologies avancées pour isoler la voix et réduire les bruits de fond. 
        Cela peut prendre quelques instants.
    """)
    with st.spinner("Nettoyage de l'audio en cours..."):
        original_signal, cleaned_signal, sample_rate = processor.clean_audio(
            input_audio_path, output_audio_path, config.LOW_CUTOFF, config.HIGH_CUTOFF
        )
    st.success("✅ Nettoyage terminé avec succès !")

    # Step 3: Audio playback
    st.subheader("3️⃣ Écoutez et comparez")
    col1, col2 = st.columns(2)
    with col1:
        st.write("🔊 Audio original")
        st.audio(uploaded_file, format="audio/mp3")
    with col2:
        st.write("🎧 Audio nettoyé")
        st.audio(output_audio_path, format="audio/wav")

    # Step 4: Waveform visualization
    st.subheader("4️⃣ Visualisation des formes d'onde")
    st.write("""
        La forme d'onde montre les variations du son au fil du temps. Elle vous permet de visualiser
        la différence entre l'audio original et l'audio nettoyé.
    """)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(original_signal[0], label="Signal original", color='blue', alpha=0.5)
    ax.plot(cleaned_signal[0], label="Signal nettoyé", color='orange', alpha=0.7)
    ax.set_title("Comparaison : Signal original vs Signal nettoyé")
    ax.set_xlabel("Temps (échantillons)")
    ax.set_ylabel("Amplitude")
    ax.legend()
    st.pyplot(fig)

    # Step 5: Download the cleaned audio
    st.subheader("5️⃣ Téléchargez l'audio nettoyé")
    with open(output_audio_path, "rb") as f:
        st.download_button(
            label="📥 Télécharger l'audio nettoyé",
            data=f,
            file_name="audio_nettoye.wav",
            mime="audio/wav",
        )
else:
    # Display a message if no file is uploaded
    st.info("Veuillez téléverser un fichier audio pour commencer.")

# Footer with credits and branding
st.markdown(
    """
    ---
    **Développé par HeticSolutions pour Hetic Radio** 🎙️
    """
)