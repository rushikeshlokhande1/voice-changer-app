"""
Voice effects module for applying various voice transformations.
"""

import numpy as np
import librosa
from scipy import signal
from pedalboard import Pedalboard, Chorus, Reverb, Distortion, Phaser
from typing import Optional


def pitch_shift(audio: np.ndarray, sr: int, semitones: float) -> np.ndarray:
    """
    Shift the pitch of audio by a number of semitones.
    
    Args:
        audio: Input audio data
        sr: Sample rate
        semitones: Number of semitones to shift (positive = higher, negative = lower)
    
    Returns:
        Pitch-shifted audio
    """
    try:
        shifted = librosa.effects.pitch_shift(audio, sr=sr, n_steps=semitones)
        return shifted
    except Exception as e:
        print(f"Warning: Pitch shift failed: {str(e)}")
        return audio


def time_stretch(audio: np.ndarray, rate: float) -> np.ndarray:
    """
    Change the speed of audio without changing pitch.
    
    Args:
        audio: Input audio data
        rate: Speed factor (>1 = faster, <1 = slower)
    
    Returns:
        Time-stretched audio
    """
    try:
        stretched = librosa.effects.time_stretch(audio, rate=rate)
        return stretched
    except Exception as e:
        print(f"Warning: Time stretch failed: {str(e)}")
        return audio


def apply_male_to_female(audio: np.ndarray, sr: int) -> np.ndarray:
    """
    Convert male voice to female voice.
    
    Args:
        audio: Input audio data
        sr: Sample rate
    
    Returns:
        Transformed audio
    """
    # Shift pitch up by 4 semitones
    shifted = pitch_shift(audio, sr, semitones=4.0)
    
    # Apply formant shifting by resampling
    # This simulates vocal tract changes
    formant_shifted = librosa.resample(shifted, orig_sr=sr, target_sr=int(sr * 1.15))
    formant_shifted = librosa.resample(formant_shifted, orig_sr=int(sr * 1.15), target_sr=sr)
    
    # Add slight brightness
    formant_shifted = apply_brightness(formant_shifted, sr, factor=1.2)
    
    return formant_shifted


def apply_female_to_male(audio: np.ndarray, sr: int) -> np.ndarray:
    """
    Convert female voice to male voice.
    
    Args:
        audio: Input audio data
        sr: Sample rate
    
    Returns:
        Transformed audio
    """
    # Shift pitch down by 4 semitones
    shifted = pitch_shift(audio, sr, semitones=-4.0)
    
    # Apply formant shifting
    formant_shifted = librosa.resample(shifted, orig_sr=sr, target_sr=int(sr * 0.88))
    formant_shifted = librosa.resample(formant_shifted, orig_sr=int(sr * 0.88), target_sr=sr)
    
    # Reduce brightness
    formant_shifted = apply_brightness(formant_shifted, sr, factor=0.8)
    
    return formant_shifted


def apply_kid_voice(audio: np.ndarray, sr: int) -> np.ndarray:
    """
    Apply kid voice effect.
    
    Args:
        audio: Input audio data
        sr: Sample rate
    
    Returns:
        Transformed audio
    """
    # High pitch shift
    shifted = pitch_shift(audio, sr, semitones=6.0)
    
    # Speed up slightly
    faster = time_stretch(shifted, rate=1.15)
    
    # Add brightness
    bright = apply_brightness(faster, sr, factor=1.3)
    
    return bright


def apply_robot_voice(audio: np.ndarray, sr: int) -> np.ndarray:
    """
    Apply robot voice effect.
    
    Args:
        audio: Input audio data
        sr: Sample rate
    
    Returns:
        Transformed audio
    """
    # Apply vocoder-like effect using phase vocoder
    # Quantize pitch to create robotic sound
    
    # Extract pitch
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
    
    # Apply distortion for metallic sound
    board = Pedalboard([
        Distortion(drive_db=15),
        Chorus(rate_hz=1.5, depth=0.3, mix=0.5)
    ])
    
    # Process audio
    robot = board(audio, sr)
    
    # Add slight pitch quantization
    robot = pitch_shift(robot, sr, semitones=0.5)
    
    # Reduce dynamic range (compression effect)
    robot = np.tanh(robot * 2.0) * 0.8
    
    return robot


def apply_anime_voice(audio: np.ndarray, sr: int) -> np.ndarray:
    """
    Apply anime-style voice effect.
    
    Args:
        audio: Input audio data
        sr: Sample rate
    
    Returns:
        Transformed audio
    """
    # High pitch
    shifted = pitch_shift(audio, sr, semitones=5.0)
    
    # Add brightness and clarity
    bright = apply_brightness(shifted, sr, factor=1.4)
    
    # Add slight reverb for "cute" effect
    board = Pedalboard([
        Reverb(room_size=0.3, damping=0.5, wet_level=0.15)
    ])
    
    anime = board(bright, sr)
    
    return anime


def apply_echo_effect(audio: np.ndarray, sr: int, delay: float = 0.3, decay: float = 0.5) -> np.ndarray:
    """
    Apply echo/delay effect.
    
    Args:
        audio: Input audio data
        sr: Sample rate
        delay: Delay time in seconds
        decay: Decay factor (0-1)
    
    Returns:
        Audio with echo effect
    """
    # Calculate delay in samples
    delay_samples = int(delay * sr)
    
    # Create output array
    output = np.zeros(len(audio) + delay_samples)
    output[:len(audio)] = audio
    
    # Add delayed signal
    output[delay_samples:delay_samples + len(audio)] += audio * decay
    
    # Normalize
    output = output / np.max(np.abs(output))
    
    return output[:len(audio)]


def apply_brightness(audio: np.ndarray, sr: int, factor: float = 1.2) -> np.ndarray:
    """
    Adjust the brightness (high-frequency content) of audio.
    
    Args:
        audio: Input audio data
        sr: Sample rate
        factor: Brightness factor (>1 = brighter, <1 = darker)
    
    Returns:
        Brightness-adjusted audio
    """
    # Design a high-shelf filter
    nyquist = sr / 2
    cutoff = 2000  # Hz
    
    # Create filter coefficients
    b, a = signal.butter(2, cutoff / nyquist, btype='high')
    
    # Apply filter
    high_freq = signal.filtfilt(b, a, audio)
    
    # Mix with original
    if factor > 1:
        # Boost high frequencies
        result = audio + high_freq * (factor - 1) * 0.3
    else:
        # Reduce high frequencies
        result = audio - high_freq * (1 - factor) * 0.3
    
    # Normalize
    result = np.clip(result, -1.0, 1.0)
    
    return result


def apply_celebrity_style(audio: np.ndarray, sr: int, style: str = "deep") -> np.ndarray:
    """
    Apply celebrity-inspired voice styles.
    
    Args:
        audio: Input audio data
        sr: Sample rate
        style: Style name ("deep", "smooth", "energetic")
    
    Returns:
        Styled audio
    """
    if style == "deep":
        # Deep, authoritative voice
        result = pitch_shift(audio, sr, semitones=-3.0)
        result = apply_brightness(result, sr, factor=0.7)
        
    elif style == "smooth":
        # Smooth, radio-host style
        result = pitch_shift(audio, sr, semitones=-1.5)
        board = Pedalboard([
            Reverb(room_size=0.2, damping=0.7, wet_level=0.1)
        ])
        result = board(result, sr)
        
    elif style == "energetic":
        # Energetic, upbeat voice
        result = pitch_shift(audio, sr, semitones=2.0)
        result = time_stretch(result, rate=1.1)
        result = apply_brightness(result, sr, factor=1.3)
        
    else:
        result = audio
    
    return result
