"""
Text-to-Speech engine using free, open-source models.
Supports both fast (pyttsx3) and realistic (Bark) voices.
"""

import numpy as np
import pyttsx3
from typing import Optional, Tuple, Dict, List
import warnings
import tempfile

# Suppress warnings
warnings.filterwarnings('ignore')

# Try to import Bark TTS
try:
    from utils.bark_tts import (
        BarkTTSEngine, 
        is_bark_available, 
        get_personality_categories
    )
    BARK_AVAILABLE = is_bark_available()
except ImportError:
    BARK_AVAILABLE = False


class UnifiedTTSEngine:
    """Unified TTS engine supporting both fast and realistic voices."""
    
    def __init__(self):
        """Initialize TTS engines."""
        self.pyttsx3_engine = None
        self.bark_engine = None
        
        # Initialize pyttsx3
        self._init_pyttsx3()
        
        # Initialize Bark if available
        if BARK_AVAILABLE:
            try:
                self.bark_engine = BarkTTSEngine()
            except Exception as e:
                print(f"Warning: Could not initialize Bark TTS: {str(e)}")
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3 engine."""
        try:
            self.pyttsx3_engine = pyttsx3.init()
            self.pyttsx3_engine.setProperty('rate', 150)
            self.pyttsx3_engine.setProperty('volume', 0.9)
        except Exception as e:
            print(f"Warning: Could not initialize pyttsx3: {str(e)}")
    
    def generate_speech(
        self,
        text: str,
        output_path: str,
        engine: str = "fast",
        voice_preset: str = "Male (Default)",
        rate: int = 150
    ) -> str:
        """
        Generate speech from text using selected engine.
        
        Args:
            text: Input text to convert to speech
            output_path: Path to save the audio file
            engine: "fast" (pyttsx3) or "realistic" (Bark)
            voice_preset: Voice preset name
            rate: Speech rate (for pyttsx3 only)
        
        Returns:
            Path to the generated audio file
        """
        if engine == "realistic" and self.bark_engine:
            return self._generate_bark(text, output_path, voice_preset)
        else:
            return self._generate_pyttsx3(text, output_path, voice_preset, rate)
    
    def _generate_bark(self, text: str, output_path: str, personality: str) -> str:
        """Generate speech using Bark TTS."""
        try:
            audio_array, sr = self.bark_engine.generate_speech(
                text, 
                personality, 
                output_path
            )
            return output_path
        except Exception as e:
            raise RuntimeError(f"Error generating Bark speech: {str(e)}")
    
    def _generate_pyttsx3(
        self, 
        text: str, 
        output_path: str, 
        voice_type: str, 
        rate: int
    ) -> str:
        """Generate speech using pyttsx3."""
        if not self.pyttsx3_engine:
            raise RuntimeError("pyttsx3 engine not initialized")
        
        try:
            voices = self.pyttsx3_engine.getProperty('voices')
            
            # Select voice based on type
            if voice_type == "Female" and len(voices) > 1:
                self.pyttsx3_engine.setProperty('voice', voices[1].id)
            elif voice_type == "Male (Default)" and len(voices) > 0:
                self.pyttsx3_engine.setProperty('voice', voices[0].id)
            else:
                if len(voices) > 0:
                    self.pyttsx3_engine.setProperty('voice', voices[0].id)
            
            # Set speech rate
            self.pyttsx3_engine.setProperty('rate', rate)
            
            # Save to file
            self.pyttsx3_engine.save_to_file(text, output_path)
            self.pyttsx3_engine.runAndWait()
            
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"Error generating pyttsx3 speech: {str(e)}")
    
    def get_available_voices(self, engine: str = "fast") -> List[str]:
        """
        Get list of available voices for selected engine.
        
        Args:
            engine: "fast" or "realistic"
        
        Returns:
            List of voice names
        """
        if engine == "realistic" and self.bark_engine:
            return self.bark_engine.get_personalities()
        else:
            return list(get_fast_voice_presets().keys())
    
    def is_bark_available(self) -> bool:
        """Check if Bark TTS is available."""
        return self.bark_engine is not None


# Legacy functions for compatibility
class TTSEngine:
    """Legacy TTS engine wrapper."""
    
    def __init__(self):
        """Initialize TTS engine."""
        self.engine = None
        self._init_pyttsx3()
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3 engine."""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
        except Exception as e:
            print(f"Warning: Could not initialize pyttsx3: {str(e)}")
    
    def generate_speech(
        self,
        text: str,
        output_path: str,
        voice_type: str = "default",
        rate: int = 150,
        pitch: int = 100
    ) -> str:
        """Generate speech from text."""
        if not self.engine:
            raise RuntimeError("TTS engine not initialized")
        
        try:
            voices = self.engine.getProperty('voices')
            
            if voice_type == "female" and len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
            elif voice_type == "male" and len(voices) > 0:
                self.engine.setProperty('voice', voices[0].id)
            else:
                if len(voices) > 0:
                    self.engine.setProperty('voice', voices[0].id)
            
            self.engine.setProperty('rate', rate)
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"Error generating speech: {str(e)}")
    
    def get_available_voices(self) -> list:
        """Get list of available voices."""
        if not self.engine:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            return [{"id": v.id, "name": v.name, "languages": v.languages} for v in voices]
        except:
            return []


def generate_tts(
    text: str,
    output_path: str,
    voice_type: str = "default",
    rate: int = 150
) -> str:
    """
    Convenience function to generate TTS (legacy).
    
    Args:
        text: Input text
        output_path: Output file path
        voice_type: Voice type ("male", "female", "default")
        rate: Speech rate
    
    Returns:
        Path to generated audio file
    """
    engine = TTSEngine()
    return engine.generate_speech(text, output_path, voice_type, rate)


def get_fast_voice_presets() -> Dict[str, Dict]:
    """
    Get predefined fast voice presets (pyttsx3).
    
    Returns:
        Dictionary of voice presets
    """
    return {
        "Male (Default)": {"voice_type": "male", "rate": 150},
        "Female": {"voice_type": "female", "rate": 155},
        "Male (Slow)": {"voice_type": "male", "rate": 120},
        "Female (Slow)": {"voice_type": "female", "rate": 125},
        "Male (Fast)": {"voice_type": "male", "rate": 180},
        "Female (Fast)": {"voice_type": "female", "rate": 185},
        "Narrator": {"voice_type": "male", "rate": 140},
        "Storyteller": {"voice_type": "female", "rate": 135},
    }


def get_voice_presets() -> Dict[str, Dict]:
    """Legacy function - returns fast voice presets."""
    return get_fast_voice_presets()


def get_realistic_voice_presets() -> Dict[str, List[str]]:
    """
    Get realistic voice presets organized by category.
    
    Returns:
        Dictionary of category -> list of personalities
    """
    if BARK_AVAILABLE:
        return get_personality_categories()
    else:
        return {}


def is_realistic_voices_available() -> bool:
    """Check if realistic voices (Bark) are available."""
    return BARK_AVAILABLE
