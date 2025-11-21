"""
Generate a sample audio file for testing.
"""

import numpy as np
import soundfile as sf

# Generate a simple test tone
sr = 22050  # Sample rate
duration = 3  # seconds

# Create a simple melody
t = np.linspace(0, duration, int(sr * duration))

# Mix of frequencies to simulate voice
freq1 = 220  # A3
freq2 = 330  # E4
freq3 = 440  # A4

audio = (
    np.sin(2 * np.pi * freq1 * t) * 0.3 +
    np.sin(2 * np.pi * freq2 * t) * 0.2 +
    np.sin(2 * np.pi * freq3 * t) * 0.1
)

# Add some envelope to make it more natural
envelope = np.exp(-t / 2)
audio = audio * envelope

# Normalize
audio = audio / np.max(np.abs(audio)) * 0.8

# Save
sf.write('examples/sample.wav', audio, sr)
print("Sample audio file created: examples/sample.wav")
