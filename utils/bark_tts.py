"""
Bark TTS integration for realistic, personality-inspired voices.
Uses Suno's Bark model for natural-sounding speech generation.
"""

import numpy as np
import warnings
from typing import Optional, Dict, List
import os

# Suppress warnings
warnings.filterwarnings('ignore')

# Try to import Bark
try:
    from bark import SAMPLE_RATE as BARK_SAMPLE_RATE, generate_audio, preload_models
    BARK_AVAILABLE = True
except ImportError:
    BARK_AVAILABLE = False
    print("Bark TTS not available. Install with: pip install bark")


# Personality voice mappings (Bark speaker presets)
# 30+ Celebrity-Inspired Voice Styles (Legal & Compliant)
PERSONALITY_VOICES = {
    # 🎬 Actor-Style Voices (6 styles)
    "Heroic Deep Male": "v2/en_speaker_6",
    "Bollywood Romantic Male": "v2/en_speaker_3",
    "Action Movie Villain": "v2/en_speaker_9",
    "Calm Story Narrator": "v2/en_speaker_0",
    "Emotional Young Actor": "v2/en_speaker_5",
    "Sharp Detective Voice": "v2/en_speaker_2",
    
    # 🎤 YouTuber-Style Voices (5 styles)
    "Energetic Vlogger": "v2/en_speaker_5",
    "Tech Reviewer Tone": "v2/en_speaker_2",
    "Gaming Streamer Voice": "v2/en_speaker_4",
    "Motivational Podcast Host": "v2/en_speaker_7",
    "Funny Cartoon YouTuber": "v2/en_speaker_8",
    
    # 👧 Character Voices (4 styles)
    "Anime Girl Voice": "v2/en_speaker_8",
    "Cartoon Boy Voice": "v2/en_speaker_4",
    "Elder Storyteller": "v2/en_speaker_9",
    "AI Robot (Friendly)": "v2/en_speaker_1",
    
    # 🎧 General Voice Tones (15 styles)
    "Deep Male": "v2/en_speaker_6",
    "Soft Female": "v2/en_speaker_1",
    "Teen Casual": "v2/en_speaker_4",
    "Child Voice": "v2/en_speaker_8",
    "Old Man Voice": "v2/en_speaker_9",
    "Professional Female": "v2/en_speaker_1",
    "Energetic Male": "v2/en_speaker_5",
    "Mysterious Whisper": "v2/en_speaker_3",
    "Radio Announcer": "v2/en_speaker_0",
    "Audiobook Reader": "v2/en_speaker_0",
    "News Reporter": "v2/en_speaker_2",
    "Sports Commentator": "v2/en_speaker_5",
    "Meditation Guide": "v2/en_speaker_3",
    "Fitness Coach": "v2/en_speaker_7",
    "ASMR Whisper": "v2/en_speaker_1",
}

# Voice style descriptions for UI
VOICE_DESCRIPTIONS = {
    # Actor-Style
    "Heroic Deep Male": "Deep, commanding superhero-style voice - perfect for epic narration",
    "Bollywood Romantic Male": "Warm, expressive, musical voice - great for romantic content",
    "Action Movie Villain": "Dark, menacing, powerful voice - dramatic and intense",
    "Calm Story Narrator": "Soothing, clear documentary-style voice - professional narration",
    "Emotional Young Actor": "Expressive, dramatic, intense voice - emotional storytelling",
    "Sharp Detective Voice": "Quick, intelligent, observant voice - mystery and investigation",
    
    # YouTuber-Style
    "Energetic Vlogger": "Upbeat, enthusiastic, friendly voice - perfect for vlogs",
    "Tech Reviewer Tone": "Clear, analytical, professional voice - tech content",
    "Gaming Streamer Voice": "Excited, dynamic, engaging voice - gaming commentary",
    "Motivational Podcast Host": "Inspiring, confident, warm voice - motivational content",
    "Funny Cartoon YouTuber": "Playful, exaggerated, comedic voice - entertainment",
    
    # Character
    "Anime Girl Voice": "High-pitched, cute, expressive voice - anime characters",
    "Cartoon Boy Voice": "Young, energetic, playful voice - cartoon characters",
    "Elder Storyteller": "Wise, aged, gentle voice - folklore and wisdom",
    "AI Robot (Friendly)": "Synthetic but warm, helpful voice - AI assistant style",
    
    # General Tones
    "Deep Male": "Rich, authoritative bass voice - professional and commanding",
    "Soft Female": "Gentle, soothing, calm voice - relaxing content",
    "Teen Casual": "Young, relaxed, conversational voice - casual content",
    "Child Voice": "Innocent, high-pitched, playful voice - children's content",
    "Old Man Voice": "Aged, wise, experienced voice - elder perspective",
    "Professional Female": "Clear, confident, business voice - corporate content",
    "Energetic Male": "Dynamic, fast-paced, lively voice - high-energy content",
    "Mysterious Whisper": "Quiet, intriguing, secretive voice - mystery content",
    "Radio Announcer": "Smooth, polished, broadcast-quality voice - radio style",
    "Audiobook Reader": "Clear, consistent, pleasant voice - long-form reading",
    "News Reporter": "Neutral, clear, informative voice - news and updates",
    "Sports Commentator": "Excited, fast, energetic voice - sports coverage",
    "Meditation Guide": "Calm, slow, peaceful voice - meditation and relaxation",
    "Fitness Coach": "Motivating, energetic, encouraging voice - workout content",
    "ASMR Whisper": "Soft, gentle, relaxing voice - ASMR content",
}

# Voice categories for organized UI
VOICE_CATEGORIES = {
    "🎬 Actor-Style": [
        "Heroic Deep Male",
        "Bollywood Romantic Male",
        "Action Movie Villain",
        "Calm Story Narrator",
        "Emotional Young Actor",
        "Sharp Detective Voice"
    ],
    "🎤 YouTuber-Style": [
        "Energetic Vlogger",
        "Tech Reviewer Tone",
        "Gaming Streamer Voice",
        "Motivational Podcast Host",
        "Funny Cartoon YouTuber"
    ],
    "👧 Character Voices": [
        "Anime Girl Voice",
        "Cartoon Boy Voice",
        "Elder Storyteller",
        "AI Robot (Friendly)"
    ],
    "🎧 General Tones": [
        "Deep Male",
        "Soft Female",
        "Teen Casual",
        "Child Voice",
        "Old Man Voice",
        "Professional Female",
        "Energetic Male",
        "Mysterious Whisper",
        "Radio Announcer",
        "Audiobook Reader",
        "News Reporter",
        "Sports Commentator",
        "Meditation Guide",
        "Fitness Coach",
        "ASMR Whisper"
    ]
}


class BarkTTSEngine:
    """Bark TTS engine for realistic voice generation."""
    
    def __init__(self):
        """Initialize Bark TTS engine."""
        self.available = BARK_AVAILABLE
        self.models_loaded = False
        
        if self.available:
            try:
                # Preload models on initialization (optional, for faster first generation)
                # Commented out to save memory - models load on first use
                # preload_models()
                # self.models_loaded = True
                pass
            except Exception as e:
                print(f"Warning: Could not preload Bark models: {str(e)}")
    
    def generate_speech(
        self,
        text: str,
        personality: str = "News Anchor (Male)",
        output_path: Optional[str] = None
    ) -> tuple:
        """
        Generate speech using Bark TTS with personality preset.
        
        Args:
            text: Input text to convert to speech
            personality: Personality preset name
            output_path: Optional path to save audio
        
        Returns:
            Tuple of (audio_array, sample_rate)
        """
        if not self.available:
            raise RuntimeError("Bark TTS not available. Install with: pip install bark")
        
        try:
            # Get speaker preset for personality
            speaker = PERSONALITY_VOICES.get(personality, "v2/en_speaker_0")
            
            # Limit text length for reasonable generation time
            if len(text) > 500:
                text = text[:500] + "..."
            
            # Generate audio with Bark
            # Format: "text [speaker_preset]"
            prompt = f"{text}"
            
            # Generate audio
            audio_array = generate_audio(
                prompt,
                history_prompt=speaker,
                text_temp=0.7,
                waveform_temp=0.7
            )
            
            # Save if output path provided
            if output_path:
                import soundfile as sf
                sf.write(output_path, audio_array, BARK_SAMPLE_RATE)
            
            return audio_array, BARK_SAMPLE_RATE
            
        except Exception as e:
            raise RuntimeError(f"Error generating speech with Bark: {str(e)}")
    
    def get_personalities(self) -> List[str]:
        """
        Get list of available personality presets.
        
        Returns:
            List of personality names
        """
        return list(PERSONALITY_VOICES.keys())
    
    def get_personality_description(self, personality: str) -> str:
        """
        Get description of a personality preset.
        
        Args:
            personality: Personality name
        
        Returns:
            Description string
        """
        descriptions = {
            "News Anchor (Male)": "Clear, authoritative, neutral tone - perfect for announcements",
            "News Anchor (Female)": "Professional, clear, confident delivery",
            "Radio Host (Male)": "Warm, engaging, smooth voice - great for podcasts",
            "Corporate Presenter": "Professional, measured, business-appropriate",
            "Energetic YouTuber": "Upbeat, enthusiastic, dynamic - perfect for content",
            "Gaming Streamer": "Excited, expressive, engaging commentary style",
            "Podcast Host (Male)": "Conversational, friendly, relaxed tone",
            "Podcast Host (Female)": "Warm, approachable, natural conversation",
            "Storyteller (Deep)": "Dramatic, engaging, varied pace - great for narratives",
            "Documentary Narrator": "Deep, calm, informative - educational content",
            "Audiobook Reader (Male)": "Clear, pleasant, consistent reading voice",
            "Audiobook Reader (Female)": "Smooth, engaging, easy to listen to",
            "Calm & Soothing": "Gentle, relaxing, slow-paced - meditation friendly",
            "Motivational Speaker": "Inspiring, powerful, emphatic delivery",
            "Friendly Conversational": "Natural, casual, like talking to a friend",
            "Professional Warm": "Professional yet approachable, trustworthy",
        }
        return descriptions.get(personality, "Realistic AI-generated voice")


def generate_bark_tts(
    text: str,
    personality: str = "News Anchor (Male)",
    output_path: Optional[str] = None
) -> tuple:
    """
    Convenience function to generate Bark TTS.
    
    Args:
        text: Input text
        personality: Personality preset
        output_path: Optional output file path
    
    Returns:
        Tuple of (audio_array, sample_rate)
    """
    engine = BarkTTSEngine()
    return engine.generate_speech(text, personality, output_path)


def is_bark_available() -> bool:
    """Check if Bark TTS is available."""
    return BARK_AVAILABLE


def get_personality_categories() -> Dict[str, List[str]]:
    """
    Get personalities organized by category.
    
    Returns:
        Dictionary of category -> list of personalities
    """
    return VOICE_CATEGORIES


def get_voice_description(personality: str) -> str:
    """
    Get description for a voice personality.
    
    Args:
        personality: Voice personality name
    
    Returns:
        Description string
    """
    return VOICE_DESCRIPTIONS.get(personality, "Celebrity-inspired voice style")


def get_all_voice_styles() -> List[str]:
    """
    Get flat list of all voice styles.
    
    Returns:
        List of all voice style names
    """
    return list(PERSONALITY_VOICES.keys())
