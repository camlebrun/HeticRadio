import torch
import librosa
import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter
from demucs import pretrained
from demucs.apply import apply_model


class AudioProcessor:
    def __init__(self, device="cpu"):
        self.device = torch.device(device)
        print(f"Using device: {self.device}")
        self.demucs = pretrained.get_model('htdemucs')
        self.demucs.to(self.device)

    @staticmethod
    def butter_lowpass_filter(data, cutoff, sr, order=5):
        nyquist = 0.5 * sr
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return lfilter(b, a, data)

    @staticmethod
    def butter_highpass_filter(data, cutoff, sr, order=3):
        nyquist = 0.5 * sr
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return lfilter(b, a, data)

    def clean_audio(self, input_audio_path, output_audio_path, low_cutoff=100, high_cutoff=3000):
        # Load MP3 audio using librosa
        print("Loading MP3 file using librosa...")
        waveform_np, sample_rate = librosa.load(input_audio_path, sr=None, mono=False)

        # Ensure audio is stereo
        if waveform_np.ndim == 1:
            waveform_np = np.array([waveform_np, waveform_np])  # Convert mono to stereo by duplicating

        # Convert waveform to PyTorch tensor with specified dtype and move to the desired device
        waveform = torch.tensor(waveform_np, dtype=torch.float32).unsqueeze(0).to(self.device)

        # Apply Demucs to isolate sources
        print("Applying Demucs for noise reduction...")
        with torch.no_grad():
            sources = apply_model(self.demucs, waveform, device=self.device)

        # Separate the sources
        vocals = sources[0][0].cpu().numpy()  # Voice channel
        noise = sources[0][1].cpu().numpy()  # Background noise channel

        # Reduce noise by subtracting it from the original audio
        cleaned_audio = waveform_np - noise

        # Apply high-pass and low-pass filters for additional noise reduction
        print("Applying high-pass and low-pass filters...")
        cleaned_audio = self.butter_highpass_filter(cleaned_audio, low_cutoff, sample_rate)
        cleaned_audio = self.butter_lowpass_filter(cleaned_audio, high_cutoff, sample_rate)

        # Save the cleaned audio
        sf.write(output_audio_path, cleaned_audio.T, sample_rate)  # Transpose for (length, channels)
        print(f"Cleaned audio saved to {output_audio_path}")

        # Return the original waveform, the cleaned audio, and the sample rate
        return waveform_np, cleaned_audio, sample_rate