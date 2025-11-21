"""
Audio utility functions for loading, saving, and processing audio files.
"""

import numpy as np
import soundfile as sf
import librosa
import noisereduce as nr
from typing import Tuple, Optional


def load_audio(file_path: str, sr: int = 22050) -> Tuple[np.ndarray, int]:
    """
    Load an audio file and return the audio data and sample rate.
    
    Args:
        file_path: Path to the audio file
        sr: Target sample rate (default: 22050 Hz)
    
    Returns:
        Tuple of (audio_data, sample_rate)
    """
    try:
        # Load audio file
        audio, sample_rate = librosa.load(file_path, sr=sr, mono=True)
        return audio, sample_rate
    except Exception as e:
        raise ValueError(f"Error loading audio file: {str(e)}")


def save_audio(audio: np.ndarray, sr: int, output_path: str) -> str:
    """
    Save audio data to a file.
    
    Args:
        audio: Audio data as numpy array
        sr: Sample rate
        output_path: Path to save the audio file
    
    Returns:
        Path to the saved file
    """
    try:
        # Normalize audio to prevent clipping
        audio = np.clip(audio, -1.0, 1.0)
        
        # Save audio file
        sf.write(output_path, audio, sr)
        return output_path
    except Exception as e:
        raise ValueError(f"Error saving audio file: {str(e)}")


def apply_noise_reduction(audio: np.ndarray, sr: int, strength: float = 0.5) -> np.ndarray:
    """
    Apply noise reduction to audio.
    
    Args:
        audio: Input audio data
        sr: Sample rate
        strength: Noise reduction strength (0.0 to 1.0)
    
    Returns:
        Denoised audio data
    """
    try:
        # Apply noise reduction
        reduced_noise = nr.reduce_noise(
            y=audio,
            sr=sr,
            prop_decrease=strength,
            stationary=True
        )
        return reduced_noise
    except Exception as e:
        print(f"Warning: Noise reduction failed: {str(e)}")
        return audio


def normalize_audio(audio: np.ndarray, target_level: float = -20.0) -> np.ndarray:
    """
    Normalize audio to a target level in dB.
    
    Args:
        audio: Input audio data
        target_level: Target level in dB
    
    Returns:
        Normalized audio data
    """
    # Calculate current RMS level
    rms = np.sqrt(np.mean(audio**2))
    
    if rms > 0:
        # Convert target level from dB to linear
        target_linear = 10 ** (target_level / 20.0)
        
        # Calculate scaling factor
        scaling_factor = target_linear / rms
        
        # Apply normalization
        normalized = audio * scaling_factor
        
        # Prevent clipping
        normalized = np.clip(normalized, -1.0, 1.0)
        
        return normalized
    else:
        return audio


def convert_to_mono(audio: np.ndarray) -> np.ndarray:
    """
    Convert stereo audio to mono.
    
    Args:
        audio: Input audio data (can be stereo or mono)
    
    Returns:
        Mono audio data
    """
    if len(audio.shape) > 1:
        # Average all channels
        return np.mean(audio, axis=1)
    return audio


def get_audio_duration(audio: np.ndarray, sr: int) -> float:
    """
    Get the duration of audio in seconds.
    
    Args:
        audio: Audio data
        sr: Sample rate
    
    Returns:
        Duration in seconds
    """
    return len(audio) / sr


def validate_audio(audio: np.ndarray, sr: int, max_duration: float = 300.0) -> bool:
    """
    Validate audio data.
    
    Args:
        audio: Audio data
        sr: Sample rate
        max_duration: Maximum allowed duration in seconds
    
    Returns:
        True if valid, raises ValueError otherwise
    """
    if audio is None or len(audio) == 0:
        raise ValueError("Audio data is empty")
    
    duration = get_audio_duration(audio, sr)
    if duration > max_duration:
        raise ValueError(f"Audio too long: {duration:.1f}s (max: {max_duration}s)")
    
    if duration < 0.1:
        raise ValueError(f"Audio too short: {duration:.1f}s (min: 0.1s)")
    
    return True
