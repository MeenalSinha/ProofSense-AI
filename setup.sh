#!/bin/bash
# ProofSense AI - Setup Script

echo "🔍 ProofSense AI - Setup Script"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python is installed"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "⚠️ Standard installation failed. Trying with --user flag..."
    pip3 install --user -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "⚠️ User installation failed. Trying with --break-system-packages (Ubuntu 24)..."
        pip3 install --break-system-packages -r requirements.txt
    fi
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "To run ProofSense AI:"
echo "  streamlit run proofsense_app.py"
echo ""
echo "Or test the core engine:"
echo "  python3 proofsense_core.py"
echo ""
echo "For detailed instructions, see README.md and QUICKSTART.md"
