# 🚀 Quick Deployment Guide for Hugging Face Spaces

## Step-by-Step Instructions

### Option 1: Web Upload (Recommended for Beginners)

1. **Go to Hugging Face Spaces**
   - Visit: https://huggingface.co/spaces
   - Sign in or create a free account

2. **Create New Space**
   - Click "Create new Space"
   - Fill in the details:
     - **Name**: `voice-changer-tts` (or your choice)
     - **License**: MIT
     - **SDK**: Select **Gradio**
     - **Hardware**: Select **CPU basic** (FREE)
     - **Visibility**: Public

3. **Upload Files**
   Click "Files" → "Add file" → "Upload files"
   
   Upload these files in order:
   ```
   ✅ app.py
   ✅ requirements.txt
   ✅ README_HF.md (rename to README.md after upload)
   ✅ utils/__init__.py
   ✅ utils/audio_utils.py
   ✅ utils/voice_effects.py
   ✅ utils/tts_engine.py
   ```

4. **Wait for Build**
   - The Space will automatically build (2-5 minutes)
   - Watch the "Building" status at the top
   - Once complete, your app is LIVE! 🎉

5. **Share Your App**
   - Your URL: `https://huggingface.co/spaces/YOUR_USERNAME/voice-changer-tts`
   - Share it with anyone!

---

### Option 2: Git Upload (For Advanced Users)

1. **Create Space** (same as above)

2. **Clone Repository**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/voice-changer-tts
   cd voice-changer-tts
   ```

3. **Copy Files**
   ```bash
   # Copy all project files to the cloned directory
   # Windows PowerShell:
   Copy-Item -Path "C:\path\to\voice-changer-app\*" -Destination . -Recurse
   
   # Or manually copy:
   # - app.py
   # - requirements.txt
   # - utils/ folder
   # - README_HF.md (rename to README.md)
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "Initial commit: Voice Changer + TTS App"
   git push
   ```

5. **Done!** Your app will build automatically.

---

## 📋 File Checklist

Before deploying, ensure you have:

- [x] `app.py` - Main application
- [x] `requirements.txt` - Dependencies
- [x] `utils/__init__.py` - Package init
- [x] `utils/audio_utils.py` - Audio utilities
- [x] `utils/voice_effects.py` - Voice effects
- [x] `utils/tts_engine.py` - TTS engine
- [x] `README.md` - Documentation (use README_HF.md)

---

## ⚙️ Hugging Face Space Settings

After creating your Space, you can configure:

### In Space Settings:
- **Hardware**: CPU basic (FREE) - Perfect for this app
- **Sleep time**: Default (48 hours) - App sleeps after inactivity
- **Visibility**: Public or Private

### Environment Variables (Optional):
None required for this app! Everything works out of the box.

---

## 🐛 Troubleshooting

### Build Fails
- **Check**: All files uploaded correctly
- **Check**: `requirements.txt` is valid
- **Solution**: Look at build logs in the Space

### App Not Loading
- **Wait**: First build takes 3-5 minutes
- **Refresh**: Try refreshing the page
- **Check**: Build logs for errors

### Voice Effects Not Working
- **Normal**: First run may be slow as libraries initialize
- **Wait**: Give it 30 seconds on first use

---

## 🎯 Testing Your Deployed App

Once deployed, test these features:

1. **Voice Conversion**
   - Upload a short audio file
   - Try "Male → Female" effect
   - Download and listen

2. **Text-to-Speech**
   - Enter: "Hello, this is a test"
   - Select "Male (Default)"
   - Generate and download

3. **Noise Reduction**
   - Upload any audio
   - Set strength to 50%
   - Apply and compare

---

## 📱 Sharing Your App

Your app URL will be:
```
https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
```

Share it on:
- Twitter/X
- LinkedIn
- Reddit
- Discord
- Your portfolio!

---

## 💡 Tips

1. **First Load**: May take 10-20 seconds as libraries initialize
2. **Audio Files**: Keep under 5 minutes for best performance
3. **Text Length**: Keep under 1000 characters for TTS
4. **Updates**: Push new commits to update your Space automatically

---

## 🎉 You're Done!

Your Voice Changer + TTS app is now live and accessible to anyone!

**Next Steps:**
- Test all features
- Share with friends
- Customize the code
- Add more voice effects

---

**Need Help?**
- Check Gradio docs: https://gradio.app/docs/
- Hugging Face Spaces guide: https://huggingface.co/docs/hub/spaces
- Open an issue on GitHub
