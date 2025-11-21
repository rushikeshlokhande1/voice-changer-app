"""
Voice Changer + Text-to-Speech Web Application

A complete web app for voice transformation and text-to-speech synthesis
using 100% free, open-source tools.

Features:
- Voice conversion (Male/Female, Kid, Robot, Anime, Celebrity styles)
- Text-to-Speech with 30+ celebrity-inspired voice styles
- Batch processing (up to 30 files)
- Noise reduction
- Audio upload/download
"""

import gradio as gr
import numpy as np
import os
import tempfile
from datetime import datetime
from pathlib import Path

# Import utility functions
from utils.audio_utils import (
    load_audio,
    save_audio,
    apply_noise_reduction,
    normalize_audio,
    validate_audio
)
from utils.voice_effects import (
    apply_male_to_female,
    apply_female_to_male,
    apply_kid_voice,
    apply_robot_voice,
    apply_anime_voice,
    apply_celebrity_style,
    apply_echo_effect
)
from utils.tts_engine import (
    UnifiedTTSEngine,
    get_fast_voice_presets,
    get_realistic_voice_presets,
    is_realistic_voices_available
)
from utils.bark_tts import (
    get_personality_categories,
    get_voice_description,
    get_all_voice_styles
)
from utils.batch_processor import (
    BatchProcessor,
    validate_audio_files,
    get_batch_summary
)


# Constants
SAMPLE_RATE = 22050
MAX_DURATION = 300  # 5 minutes
MAX_BATCH_FILES = 30  # Maximum files for batch processing

# Initialize TTS engine
tts_engine = UnifiedTTSEngine()
BARK_AVAILABLE = tts_engine.is_bark_available()


def process_voice_conversion(audio_file, effect_type):
    """
    Process voice conversion with selected effect.
    
    Args:
        audio_file: Uploaded audio file path
        effect_type: Type of voice effect to apply
    
    Returns:
        Tuple of (output_audio_path, status_message)
    """
    try:
        if audio_file is None:
            return None, "❌ Please upload an audio file first!"
        
        # Load audio
        audio, sr = load_audio(audio_file, sr=SAMPLE_RATE)
        
        # Validate audio
        validate_audio(audio, sr)
        
        # Apply selected effect
        if effect_type == "Male → Female":
            processed = apply_male_to_female(audio, sr)
        elif effect_type == "Female → Male":
            processed = apply_female_to_male(audio, sr)
        elif effect_type == "Kid Voice":
            processed = apply_kid_voice(audio, sr)
        elif effect_type == "Robot Voice":
            processed = apply_robot_voice(audio, sr)
        elif effect_type == "Anime Voice":
            processed = apply_anime_voice(audio, sr)
        elif effect_type == "Celebrity (Deep)":
            processed = apply_celebrity_style(audio, sr, style="deep")
        elif effect_type == "Celebrity (Smooth)":
            processed = apply_celebrity_style(audio, sr, style="smooth")
        elif effect_type == "Celebrity (Energetic)":
            processed = apply_celebrity_style(audio, sr, style="energetic")
        elif effect_type == "Echo Effect":
            processed = apply_echo_effect(audio, sr)
        else:
            return None, f"❌ Unknown effect: {effect_type}"
        
        # Normalize output
        processed = normalize_audio(processed)
        
        # Save to temporary file
        output_path = tempfile.mktemp(suffix=".wav")
        save_audio(processed, sr, output_path)
        
        return output_path, f"✅ Successfully applied {effect_type}!"
        
    except Exception as e:
        return None, f"❌ Error: {str(e)}"


def process_tts(text, voice_quality, voice_preset, speech_rate):
    """
    Generate speech from text with engine selection.
    
    Args:
        text: Input text to convert to speech
        voice_quality: "Fast" or "Realistic"
        voice_preset: Voice preset name
        speech_rate: Speech rate (words per minute, for fast voices only)
    
    Returns:
        Tuple of (output_audio_path, status_message)
    """
    try:
        if not text or len(text.strip()) == 0:
            return None, "❌ Please enter some text first!"
        
        if len(text) > 5000:
            return None, "❌ Text too long! Maximum 5000 characters."
        
        # Determine engine
        engine = "realistic" if voice_quality == "Realistic (Bark)" else "fast"
        
        # Generate TTS
        output_path = tempfile.mktemp(suffix=".wav")
        
        tts_engine.generate_speech(
            text,
            output_path,
            engine=engine,
            voice_preset=voice_preset,
            rate=speech_rate
        )
        
        quality_note = "realistic Bark TTS" if engine == "realistic" else "fast pyttsx3"
        return output_path, f"✅ Successfully generated speech with {voice_preset} ({quality_note})!"
        
    except Exception as e:
        return None, f"❌ Error: {str(e)}"


def process_noise_reduction(audio_file, reduction_strength):
    """
    Apply noise reduction to audio.
    
    Args:
        audio_file: Uploaded audio file path
        reduction_strength: Noise reduction strength (0-100)
    
    Returns:
        Tuple of (output_audio_path, status_message)
    """
    try:
        if audio_file is None:
            return None, "❌ Please upload an audio file first!"
        
        # Load audio
        audio, sr = load_audio(audio_file, sr=SAMPLE_RATE)
        
        # Validate audio
        validate_audio(audio, sr)
        
        # Apply noise reduction
        strength = reduction_strength / 100.0
        processed = apply_noise_reduction(audio, sr, strength=strength)
        
        # Normalize output
        processed = normalize_audio(processed)
        
        # Save to temporary file
        output_path = tempfile.mktemp(suffix=".wav")
        save_audio(processed, sr, output_path)
        
        return output_path, f"✅ Noise reduction applied (strength: {reduction_strength}%)!"
        
    except Exception as e:
        return None, f"❌ Error: {str(e)}"


def process_batch_conversion(files, effect_type, progress=gr.Progress()):
    """
    Process multiple audio files with the same voice effect.
    
    Args:
        files: List of uploaded audio files
        effect_type: Voice effect to apply
        progress: Gradio progress tracker
    
    Returns:
        Tuple of (zip_file_path, status_message)
    """
    try:
        if not files:
            return None, "❌ Please upload at least one audio file!"
        
        # Validate files
        is_valid, error_msg = validate_audio_files(files, MAX_BATCH_FILES)
        if not is_valid:
            return None, f"❌ {error_msg}"
        
        # Initialize batch processor
        processor = BatchProcessor()
        processor.create_temp_directory()
        
        successful_files = []
        errors = []
        
        # Process each file
        for i, file in enumerate(files):
            try:
                progress((i + 1) / len(files), desc=f"Processing {i+1}/{len(files)}")
                
                # Load audio
                audio, sr = load_audio(file, sr=SAMPLE_RATE)
                validate_audio(audio, sr)
                
                # Apply effect (same logic as single file processing)
                if effect_type == "Male → Female":
                    processed = apply_male_to_female(audio, sr)
                elif effect_type == "Female → Male":
                    processed = apply_female_to_male(audio, sr)
                elif effect_type == "Kid Voice":
                    processed = apply_kid_voice(audio, sr)
                elif effect_type == "Robot Voice":
                    processed = apply_robot_voice(audio, sr)
                elif effect_type == "Anime Voice":
                    processed = apply_anime_voice(audio, sr)
                elif effect_type == "Celebrity (Deep)":
                    processed = apply_celebrity_style(audio, sr, style="deep")
                elif effect_type == "Celebrity (Smooth)":
                    processed = apply_celebrity_style(audio, sr, style="smooth")
                elif effect_type == "Celebrity (Energetic)":
                    processed = apply_celebrity_style(audio, sr, style="energetic")
                elif effect_type == "Echo Effect":
                    processed = apply_echo_effect(audio, sr)
                else:
                    errors.append(f"File {i+1}: Unknown effect")
                    continue
                
                # Normalize and save
                processed = normalize_audio(processed)
                filename = Path(file).stem if hasattr(file, 'name') else f"file_{i+1}"
                output_path = os.path.join(processor.temp_dir, f"{filename}_processed.wav")
                save_audio(processed, sr, output_path)
                successful_files.append(output_path)
                
            except Exception as e:
                errors.append(f"File {i+1}: {str(e)}")
        
        # Create ZIP file
        if successful_files:
            zip_path = tempfile.mktemp(suffix=".zip")
            processor.create_zip(zip_path, successful_files)
            
            summary = get_batch_summary(len(successful_files), len(errors), len(files))
            return zip_path, f"{summary}\n\nDownload ZIP file with all processed audio!"
        else:
            return None, f"❌ All files failed to process:\n" + "\n".join(errors[:5])
        
    except Exception as e:
        return None, f"❌ Batch processing error: {str(e)}"


# Create Gradio Interface
def create_interface():
    """Create the Gradio web interface."""
    
    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        font-family: 'Inter', sans-serif;
        max-width: 1200px;
        margin: auto;
    }
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: 14px;
    }
    """
    
    with gr.Blocks(css=custom_css, title="Voice Changer + TTS") as app:
        
        # Header
        gr.HTML("""
        <div class="header">
            <h1>🎙️ Voice Changer + Text-to-Speech</h1>
            <p>Transform your voice and generate speech using 100% free tools!</p>
        </div>
        """)
        
        # Tabs for different features
        with gr.Tabs():
            
            # Tab 1: Voice Conversion
            with gr.Tab("🎭 Voice Conversion"):
                gr.Markdown("""
                ### Transform Your Voice
                Upload an audio file and apply amazing voice effects!
                """)
                
                with gr.Row():
                    with gr.Column():
                        vc_input = gr.Audio(
                            label="Upload Audio File",
                            type="filepath",
                            sources=["upload", "microphone"]
                        )
                        vc_effect = gr.Dropdown(
                            choices=[
                                "Male → Female",
                                "Female → Male",
                                "Kid Voice",
                                "Robot Voice",
                                "Anime Voice",
                                "Celebrity (Deep)",
                                "Celebrity (Smooth)",
                                "Celebrity (Energetic)",
                                "Echo Effect"
                            ],
                            value="Male → Female",
                            label="Select Voice Effect"
                        )
                        vc_button = gr.Button("🎵 Transform Voice", variant="primary")
                    
                    with gr.Column():
                        vc_output = gr.Audio(label="Transformed Audio")
                        vc_status = gr.Textbox(label="Status", interactive=False)
                
                vc_button.click(
                    fn=process_voice_conversion,
                    inputs=[vc_input, vc_effect],
                    outputs=[vc_output, vc_status]
                )
            
            # Tab 2: Text-to-Speech
            with gr.Tab("🗣️ Text-to-Speech"):
                gr.Markdown("""
                ### Generate Speech from Text
                Choose between **Fast** (instant) or **Realistic** (natural-sounding) voices!
                
                > ℹ️ **Voice Style Information**  
                > All realistic voices are celebrity-inspired in **style only**, not exact replicas.  
                > We use legal, open-source Bark TTS models with descriptive style names.  
                > ✅ Fully copyright compliant | ✅ Safe for commercial use | ✅ No celebrity voice cloning
                """)
                
                with gr.Row():
                    with gr.Column():
                        tts_text = gr.Textbox(
                            label="Enter Text",
                            placeholder="Type your text here...",
                            lines=5,
                            max_lines=10
                        )
                        
                        # Voice quality selector
                        tts_quality = gr.Radio(
                            choices=["Fast (pyttsx3)", "Realistic (Bark)"] if BARK_AVAILABLE else ["Fast (pyttsx3)"],
                            value="Fast (pyttsx3)",
                            label="Voice Quality",
                            info="Fast: Instant generation | Realistic: 30+ AI voice styles (5-15s)"
                        )
                        
                        # Voice preset dropdown (updates based on quality)
                        tts_voice = gr.Dropdown(
                            choices=list(get_fast_voice_presets().keys()),
                            value="Male (Default)",
                            label="Select Voice",
                            info="Choose a voice style"
                        )
                        
                        # Speech rate (only for fast voices)
                        tts_rate = gr.Slider(
                            minimum=80,
                            maximum=250,
                            value=150,
                            step=10,
                            label="Speech Rate (words/min)",
                            info="Only applies to Fast voices",
                            visible=True
                        )
                        
                        tts_button = gr.Button("🎤 Generate Speech", variant="primary")
                    
                    with gr.Column():
                        tts_output = gr.Audio(label="Generated Speech")
                        tts_status = gr.Textbox(label="Status", interactive=False)
                        
                        # Show available realistic voices if Bark is available
                        if BARK_AVAILABLE:
                            gr.Markdown("""
                            #### 🎭 Realistic Voice Personalities
                            
                            **Professional**: News Anchor, Radio Host, Corporate  
                            **Entertainment**: YouTuber, Streamer, Podcast Host  
                            **Character**: Storyteller, Narrator, Audiobook  
                            **Emotional**: Calm, Motivational, Conversational
                            """)
                        else:
                            gr.Markdown("""
                            ℹ️ **Want realistic voices?**  
                            Install Bark TTS: `pip install git+https://github.com/suno-ai/bark.git`
                            """)
                
                # Update voice dropdown when quality changes
                def update_voice_choices(quality):
                    if quality == "Realistic (Bark)" and BARK_AVAILABLE:
                        realistic_presets = get_realistic_voice_presets()
                        # Flatten all categories into one list
                        all_voices = []
                        for category, voices in realistic_presets.items():
                            all_voices.extend(voices)
                        return gr.Dropdown(choices=all_voices, value=all_voices[0] if all_voices else "News Anchor (Male)")
                    else:
                        fast_presets = list(get_fast_voice_presets().keys())
                        return gr.Dropdown(choices=fast_presets, value="Male (Default)")
                
                tts_quality.change(
                    fn=update_voice_choices,
                    inputs=[tts_quality],
                    outputs=[tts_voice]
                )
                
                tts_button.click(
                    fn=process_tts,
                    inputs=[tts_text, tts_quality, tts_voice, tts_rate],
                    outputs=[tts_output, tts_status]
                )
            
            # Tab 3: Noise Reduction
            with gr.Tab("🔇 Noise Reduction"):
                gr.Markdown("""
                ### Remove Background Noise
                Upload an audio file and remove unwanted background noise!
                """)
                
                with gr.Row():
                    with gr.Column():
                        nr_input = gr.Audio(
                            label="Upload Audio File",
                            type="filepath",
                            sources=["upload", "microphone"]
                        )
                        nr_strength = gr.Slider(
                            minimum=0,
                            maximum=100,
                            value=50,
                            step=5,
                            label="Noise Reduction Strength (%)"
                        )
                        nr_button = gr.Button("🔊 Reduce Noise", variant="primary")
                    
                    with gr.Column():
                        nr_output = gr.Audio(label="Cleaned Audio")
                        nr_status = gr.Textbox(label="Status", interactive=False)
                
                nr_button.click(
                    fn=process_noise_reduction,
                    inputs=[nr_input, nr_strength],
                    outputs=[nr_output, nr_status]
                )
            
            # Tab 4: Batch Processing (NEW!)
            with gr.Tab("📦 Batch Processing"):
                gr.Markdown("""
                ### Process Multiple Files at Once
                Upload up to **30 audio files** and apply the same voice effect to all!
                
                **Features:**
                - Multi-file upload (drag & drop supported)
                - Apply same effect to all files
                - Download all processed files as ZIP
                - Progress tracking
                """)
                
                with gr.Row():
                    with gr.Column():
                        batch_input = gr.File(
                            label="Upload Multiple Audio Files (Max: 30)",
                            file_count="multiple",
                            file_types=["audio"]
                        )
                        batch_effect = gr.Dropdown(
                            choices=[
                                "Male → Female",
                                "Female → Male",
                                "Kid Voice",
                                "Robot Voice",
                                "Anime Voice",
                                "Celebrity (Deep)",
                                "Celebrity (Smooth)",
                                "Celebrity (Energetic)",
                                "Echo Effect"
                            ],
                            value="Male → Female",
                            label="Select Voice Effect (Applied to All Files)"
                        )
                        batch_button = gr.Button("🎵 Process All Files", variant="primary", size="lg")
                    
                    with gr.Column():
                        batch_output = gr.File(label="Download ZIP File")
                        batch_status = gr.Textbox(
                            label="Status",
                            interactive=False,
                            lines=5
                        )
                        gr.Markdown("""
                        **Tips:**
                        - Supported formats: WAV, MP3, M4A, FLAC, OGG
                        - Maximum 30 files per batch
                        - All files will be processed with the same effect
                        - Download ZIP contains all processed files
                        """)
                
                batch_button.click(
                    fn=process_batch_conversion,
                    inputs=[batch_input, batch_effect],
                    outputs=[batch_output, batch_status]
                )
            
            # Tab 5: About
            with gr.Tab("ℹ️ About"):
                gr.Markdown("""
                ## About This App
                
                This is a **100% free and open-source** voice changer and text-to-speech application!
                
                ### Features
                
                ✅ **Voice Conversion**
                - Male ↔ Female voice transformation
                - Kid voice effect
                - Robot voice effect
                - Anime voice effect
                - Celebrity-style voices (Deep, Smooth, Energetic)
                - Echo effects
                
                ✅ **Text-to-Speech**
                - **30+ Celebrity-Inspired Voice Styles**
                  - 🎬 Actor-Style (6): Heroic, Romantic, Villain, Narrator, etc.
                  - 🎤 YouTuber-Style (5): Vlogger, Tech Reviewer, Gamer, etc.
                  - 👧 Character (4): Anime, Cartoon, Elder, AI Robot
                  - 🎧 General Tones (15+): Deep Male, Soft Female, Teen, Child, etc.
                - Fast voices (8) - Instant generation
                - Realistic voices (30+) - Natural AI speech
                - Adjustable speech rate
                
                ✅ **Batch Processing** (NEW!)
                - Upload up to 30 audio files at once
                - Apply same effect to all files
                - Download as single ZIP file
                - Progress tracking
                
                ✅ **Noise Reduction**
                - Remove background noise
                - Adjustable reduction strength
                - Preserve voice quality
                
                ### Legal & Compliance
                
                ⚖️ **Copyright Safe**
                - All voices are style-inspired, NOT exact celebrity replicas
                - Uses legal, open-source Bark TTS models
                - Descriptive style names only
                - ✅ Fully copyright compliant
                - ✅ Safe for commercial use
                - ✅ No celebrity voice cloning
                
                ### Technologies Used
                
                - **Gradio** - Web interface
                - **Librosa** - Audio processing
                - **Pedalboard** - Audio effects
                - **pyttsx3** - Fast text-to-speech
                - **Bark TTS** - Realistic AI voices (30+ styles)
                - **noisereduce** - Noise reduction
                
                ### Deployment
                
                This app runs on **Hugging Face Spaces** for free!
                
                ### Support
                
                - Maximum audio duration: 5 minutes
                - Supported formats: WAV, MP3, M4A, FLAC, OGG
                - Sample rate: 22050 Hz
                - Batch limit: 30 files
                
                ---
                
                Made with ❤️ using 100% free and open-source tools!
                """)
        
        # Footer
        gr.HTML("""
        <div class="footer">
            <p>🚀 Powered by Gradio | 🎵 100% Free & Open Source</p>
        </div>
        """)
    
    return app


# Main entry point
if __name__ == "__main__":
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
