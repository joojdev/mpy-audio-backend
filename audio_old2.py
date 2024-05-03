import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wavfile

def read_audio(filename):
    """Read an audio file and return the sample rate and audio data."""
    rate, data = wavfile.read(filename)
    return rate, data.astype(float)

def resample_audio(data, orig_rate, target_rate=8000):
    """Resample the audio to the target rate."""
    number_of_samples = round(len(data) * float(target_rate) / orig_rate)
    resampled_data = signal.resample(data, number_of_samples)
    return resampled_data

def convert_to_mono(data):
    """Convert stereo audio data to mono."""
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    return data

def de_ess(audio, rate, threshold=0.6, ratio=0.3):
    """Reduce sibilance in the audio signal."""
    # Design a sharper high-pass filter to find sibilant frequencies above 3 kHz
    sos = signal.butter(12, 3000, 'hp', fs=rate, output='sos')  # Increased filter order for a sharper cutoff
    filtered = signal.sosfilt(sos, audio)

    # Full-wave rectification of the filtered signal
    rectified = np.abs(filtered)

    # Find where sibilance likely occurs
    sibilance_detected = rectified > (threshold * np.max(rectified))

    # Reduce the volume of these high sibilance areas
    audio[sibilance_detected] = audio[sibilance_detected] * ratio

    return audio

def quantize_to_8bit(data):
    """Quantize the audio data to 8-bit PCM."""
    # Normalize the audio to 0-1
    data = (data - data.min()) / (data.max() - data.min())
    # Scale to 0-255 and convert to uint8
    data = (data * 255).astype(np.uint8)
    return data

def write_audio(filename, rate, data):
    """Write the modified audio data to a new file."""
    wavfile.write(filename, rate, data)

def prepare_audio(filename):
    # Read the audio file
    rate, data = read_audio(filename)

    # Convert to mono if necessary
    data = convert_to_mono(data)

    # Resample the audio to 8 kHz
    data = resample_audio(data, rate)

    # De-ess the audio
    processed_data = de_ess(data, 8000)

    # Quantize the audio to 8-bit
    processed_data = quantize_to_8bit(processed_data)

    # Write the processed audio to a new file
    write_audio(filename, 8000, processed_data)
