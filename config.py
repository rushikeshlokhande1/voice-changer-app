"""
Production configuration for Voice Changer + TTS App
"""

import os
from typing import Dict, Any

# Environment detection
IS_PRODUCTION = os.getenv("SPACE_ID") is not None  # Hugging Face Spaces
IS_LOCAL = not IS_PRODUCTION

# Resource Limits
MAX_FILE_SIZE_MB = 50  # Maximum file size in MB
MAX_AUDIO_DURATION = 300  # Maximum audio duration in seconds (5 minutes)
MAX_BATCH_FILES = 30  # Maximum files in batch processing
MAX_TEXT_LENGTH = 5000  # Maximum text length for TTS

# Memory Management
ENABLE_CLEANUP = True  # Auto-cleanup temp files
CLEANUP_INTERVAL = 3600  # Cleanup interval in seconds (1 hour)
MAX_TEMP_FILES = 100  # Maximum temp files before forced cleanup

# Performance
ENABLE_CACHING = True  # Enable model caching
CACHE_TTL = 7200  # Cache time-to-live in seconds (2 hours)
CONCURRENT_REQUESTS = 5  # Maximum concurrent processing requests

# Feature Flags
ENABLE_BARK_TTS = True  # Enable Bark TTS (realistic voices)
ENABLE_BATCH_PROCESSING = True  # Enable batch processing
ENABLE_NOISE_REDUCTION = True  # Enable noise reduction
ENABLE_VOICE_CONVERSION = True  # Enable voice conversion

# Logging
LOG_LEVEL = "INFO" if IS_PRODUCTION else "DEBUG"
ENABLE_DETAILED_ERRORS = not IS_PRODUCTION  # Show detailed errors in dev only

# Gradio Configuration
GRADIO_SERVER_NAME = "0.0.0.0"
GRADIO_SERVER_PORT = 7860
GRADIO_SHARE = False  # Don't create public link
GRADIO_SHOW_ERROR = not IS_PRODUCTION  # Show errors in dev only
GRADIO_ANALYTICS_ENABLED = False  # Disable analytics

# File Handling
ALLOWED_AUDIO_FORMATS = [".wav", ".mp3", ".m4a", ".flac", ".ogg"]
OUTPUT_FORMAT = "wav"
SAMPLE_RATE = 22050

# Error Messages
ERROR_MESSAGES = {
    "file_too_large": f"❌ File too large! Maximum size: {MAX_FILE_SIZE_MB}MB",
    "audio_too_long": f"❌ Audio too long! Maximum duration: {MAX_AUDIO_DURATION} seconds",
    "invalid_format": f"❌ Invalid format! Supported: {', '.join(ALLOWED_AUDIO_FORMATS)}",
    "batch_limit": f"❌ Too many files! Maximum: {MAX_BATCH_FILES} files",
    "text_too_long": f"❌ Text too long! Maximum: {MAX_TEXT_LENGTH} characters",
    "processing_error": "❌ Processing error. Please try again.",
    "bark_not_available": "⚠️ Realistic voices not available. Install Bark TTS or use fast voices.",
}

# Success Messages
SUCCESS_MESSAGES = {
    "voice_converted": "✅ Voice conversion successful!",
    "tts_generated": "✅ Speech generated successfully!",
    "noise_reduced": "✅ Noise reduction applied!",
    "batch_complete": "✅ Batch processing complete!",
}


def get_config() -> Dict[str, Any]:
    """
    Get current configuration as dictionary.
    
    Returns:
        Configuration dictionary
    """
    return {
        "environment": "production" if IS_PRODUCTION else "development",
        "resource_limits": {
            "max_file_size_mb": MAX_FILE_SIZE_MB,
            "max_audio_duration": MAX_AUDIO_DURATION,
            "max_batch_files": MAX_BATCH_FILES,
            "max_text_length": MAX_TEXT_LENGTH,
        },
        "features": {
            "bark_tts": ENABLE_BARK_TTS,
            "batch_processing": ENABLE_BATCH_PROCESSING,
            "noise_reduction": ENABLE_NOISE_REDUCTION,
            "voice_conversion": ENABLE_VOICE_CONVERSION,
        },
        "performance": {
            "caching": ENABLE_CACHING,
            "cleanup": ENABLE_CLEANUP,
            "concurrent_requests": CONCURRENT_REQUESTS,
        }
    }


def validate_file_size(file_path: str) -> bool:
    """
    Validate file size against limit.
    
    Args:
        file_path: Path to file
    
    Returns:
        True if valid, False otherwise
    """
    try:
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        return size_mb <= MAX_FILE_SIZE_MB
    except:
        return False


def get_error_message(error_type: str) -> str:
    """
    Get user-friendly error message.
    
    Args:
        error_type: Type of error
    
    Returns:
        Error message string
    """
    return ERROR_MESSAGES.get(error_type, ERROR_MESSAGES["processing_error"])


def get_success_message(success_type: str) -> str:
    """
    Get success message.
    
    Args:
        success_type: Type of success
    
    Returns:
        Success message string
    """
    return SUCCESS_MESSAGES.get(success_type, "✅ Operation successful!")
