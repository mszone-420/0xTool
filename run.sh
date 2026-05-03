#!/bin/bash

# 0xTool Launcher Script
# Quick start for Termux

clear

echo ""
echo "╔════════════════════════════════╗"
echo "║      ⚡ Starting 0xTool ⚡      ║"
echo "╚════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ -f "app.py" ]; then
    echo "✅ Found app.py in current directory"
    echo "🚀 Launching 0xTool..."
    echo ""
    python app.py
else
    echo "⚠️ app.py not found in current directory"
    echo "📂 Trying to go to 0xTool folder..."
    
    if [ -d "$HOME/0xTool" ]; then
        cd $HOME/0xTool
        echo "✅ Found 0xTool directory"
        echo "🚀 Launching 0xTool..."
        echo ""
        python app.py
    else
        echo "❌ 0xTool not installed!"
        echo ""
        echo "Please install first:"
        echo "  bash install.sh"
        exit 1
    fi
fi
