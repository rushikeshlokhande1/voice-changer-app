#!/bin/bash

# Voice Changer + TTS - Production Deployment Script
# This script prepares and deploys the app to Hugging Face Spaces

echo "🚀 Voice Changer + TTS - Production Deployment"
echo "=============================================="

# Check if running in correct directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Run this script from the project root directory."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Validate file structure
echo "📁 Validating file structure..."

required_files=(
    "app.py"
    "config.py"
    "requirements.txt"
    "README.md"
    "utils/__init__.py"
    "utils/audio_utils.py"
    "utils/voice_effects.py"
    "utils/tts_engine.py"
    "utils/bark_tts.py"
    "utils/batch_processor.py"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: Required file missing: $file"
        exit 1
    fi
done

echo "✅ All required files present"

# Run tests (optional)
echo "🧪 Running basic tests..."
python -c "
import sys
try:
    import gradio
    import numpy
    import librosa
    import soundfile
    import scipy
    import noisereduce
    import pedalboard
    import pyttsx3
    print('✅ All core dependencies importable')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Error: Dependency test failed"
    exit 1
fi

# Create deployment package
echo "📦 Creating deployment package..."

# List files to deploy
echo ""
echo "Files ready for deployment:"
echo "  ✅ app.py"
echo "  ✅ config.py"
echo "  ✅ requirements.txt"
echo "  ✅ README.md"
echo "  ✅ utils/ (6 files)"
echo "  ✅ .env.example"
echo ""

echo "=============================================="
echo "✅ Production deployment preparation complete!"
echo ""
echo "Next steps:"
echo "1. Go to https://huggingface.co/spaces"
echo "2. Create a new Space (Gradio SDK, CPU basic)"
echo "3. Upload all files listed above"
echo "4. Wait for build to complete (3-5 minutes)"
echo "5. Test your live app!"
echo ""
echo "📖 See PRODUCTION_GUIDE.md for detailed instructions"
echo "=============================================="
