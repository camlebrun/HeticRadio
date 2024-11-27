import streamlit as st
import tempfile
import matplotlib.pyplot as plt
from audio_processor import AudioProcessor
import librosa
import librosa.display
import config

# Initialize AudioProcessor with the appropriate device
processor = AudioProcessor(device=config.DEVICE)

# Configure the Streamlit page layout and title
st.set_page_config(page_title="Analyse Audio - Hetic Radio", layout="wide")
st.title("🎵 Analyse Audio - Fait par HeticSolutions pour Hetic Radio")

# Step 1: File upload
st.header("1️⃣ Téléversez un fichier audio")
st.write("""
    Téléversez un fichier au format MP3 ou WAV pour commencer. Vous pourrez ensuite visualiser, 
    écouter et nettoyer l'audio.
""")
uploaded_file = st.file_uploader("Choisissez un fichier audio :", type=["mp3", "wav"])

if uploaded_file:
    st.info("🎤 Fichier audio téléversé avec succès !")

    # Save the uploaded file temporarily for processing
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_input:
        temp_input.write(uploaded_file.read())
        input_audio_path = temp_input.name

    # Load the audio for visualization
    with st.spinner("Analyse de l'audio en cours..."):
        original_signal, sample_rate = librosa.load(input_audio_path, sr=None)

    # Step 2: Playback and visualization of the original audio
    st.header("2️⃣ Lecture et visualisation de l'audio original")
    st.write("""
        Voici votre audio tel qu'il a été téléversé. Écoutez-le et consultez la forme d'onde pour 
        mieux comprendre sa qualité initiale.
    """)

    # Audio playback
    st.subheader("🔊 Lecture de l'audio original")
    st.audio(uploaded_file, format="audio/mp3")

    # Waveform visualization
    st.subheader("🎨 Forme d'onde de l'audio original")
    fig, ax = plt.subplots(figsize=(10, 4))
    librosa.display.waveshow(original_signal, sr=sample_rate, ax=ax)
    ax.set_title("Forme d'onde de l'audio original")
    ax.set_xlabel("Temps (secondes)")
    ax.set_ylabel("Amplitude")
    st.pyplot(fig)

    # Step 3: Clean the audio using the AudioProcessor
    st.header("3️⃣ Nettoyage de l'audio")
    st.write("""
        Nous allons maintenant nettoyer l'audio pour réduire les bruits de fond et isoler la voix. 
        Cela peut prendre quelques instants.
    """)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_output:
        output_audio_path = temp_output.name

    with st.spinner("Nettoyage de l'audio en cours..."):
        cleaned_signal, noise_signal, sample_rate = processor.clean_audio(
            input_audio_path, output_audio_path, config.LOW_CUTOFF, config.HIGH_CUTOFF
        )
    st.success("✅ Nettoyage terminé avec succès !")

    # Step 4: Compare original and cleaned audio
    st.header("4️⃣ Comparaison : Audio original vs Audio nettoyé")
    st.write("""
        Comparez l'audio original et l'audio nettoyé en écoutant et en visualisant leurs formes 
        d'onde respectives.
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.write("🔊 **Audio original**")
        st.audio(uploaded_file, format="audio/mp3")
    with col2:
        st.write("🎧 **Audio nettoyé**")
        st.audio(output_audio_path, format="audio/wav")



    # Step 5: Download the cleaned audio
    st.header("5️⃣ Téléchargez l'audio nettoyé")
    st.write("""
        Cliquez sur le bouton ci-dessous pour télécharger l'audio nettoyé et l'utiliser selon vos besoins.
    """)
    with open(output_audio_path, "rb") as f:
        st.download_button(
            label="📥 Télécharger l'audio nettoyé",
            data=f,
            file_name="audio_nettoye.wav",
            mime="audio/wav",
        )
else:
    st.info("Veuillez téléverser un fichier audio pour commencer.")

# Footer with credits and branding
st.markdown(
    """
    ---
    **Développé par HeticSolutions pour Hetic Radio** 🎙️
    """
)