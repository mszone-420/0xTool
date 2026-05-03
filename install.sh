#!/bin/bash

# 0xTool Installer Script
# One command installation for Termux

echo ""
echo "╔════════════════════════════════╗"
echo "║     ⚡ 0xTool INSTALLER ⚡      ║"
echo "║     Ultimate Media Tool        ║"
echo "╚════════════════════════════════╝"
echo ""

# Check if running in Termux
if [ -d "/data/data/com.termux" ]; then
    echo "✅ Termux detected"
else
    echo "⚠️ This tool is made for Termux"
    echo "   But you can still try on other Linux"
fi

echo ""
echo "📦 Step 1: Updating packages..."
pkg update -y && pkg upgrade -y

echo ""
echo "📦 Step 2: Installing dependencies..."
pkg install -y python ffmpeg git

echo ""
echo "📥 Step 3: Cloning 0xTool repository..."
git clone https://github.com/mszone-420/0xTool.git
echo ""
echo "📂 Step 4: Entering directory..."
cd 0xTool

echo ""
echo "🐍 Step 5: Installing Python packages..."
pip install -r requirements.txt

echo ""
echo "✅ Step 6: Installation complete!"
echo ""
echo "╔════════════════════════════════╗"
echo "║     🚀 HOW TO RUN 0xTOOL       ║"
echo "╚════════════════════════════════╝"
echo ""
echo "  cd 0xTool"
echo "  python app.py"
echo ""
echo "  Then open browser: http://localhost:5000"
echo ""
echo "⭐ Don't forget to star this repo!"
