#!/bin/bash

# Create ZIP package for deployment
echo "📦 Creating deployment package..."

# Create a clean deployment folder
mkdir -p deployment-package

# Copy required files
cp app.py deployment-package/
cp config.py deployment-package/
cp requirements.txt deployment-package/
cp README.md deployment-package/
cp .env.example deployment-package/
cp -r utils deployment-package/
cp -r examples deployment-package/

# Create ZIP
cd deployment-package
zip -r ../voice-changer-deployment.zip .
cd ..

echo "✅ Deployment package created: voice-changer-deployment.zip"
echo ""
echo "This ZIP contains all files needed for Hugging Face Spaces deployment:"
echo "  ✅ app.py"
echo "  ✅ config.py"
echo "  ✅ requirements.txt"
echo "  ✅ README.md"
echo "  ✅ utils/ (6 files)"
echo "  ✅ examples/"
echo ""
echo "Upload this ZIP to Hugging Face Spaces!"
