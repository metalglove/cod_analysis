#!/bin/bash

# COD Analysis Development Environment Setup Script
# This script sets up a Python virtual environment with all required dependencies

set -e  # Exit on any error

echo "🚀 Setting up COD Analysis Development Environment"
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version (minimum 3.8)
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version is installed, but Python $required_version or higher is required."
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment
ENV_NAME="cod_analysis_env"
echo "📦 Creating virtual environment: $ENV_NAME"

if [ -d "$ENV_NAME" ]; then
    echo "⚠️  Virtual environment already exists. Removing old environment..."
    rm -rf "$ENV_NAME"
fi

python3 -m venv "$ENV_NAME"

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source "$ENV_NAME/bin/activate"

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing requirements..."
if [ "$1" = "dev" ]; then
    echo "🔧 Installing development requirements..."
    pip install -r requirements-dev.txt
else
    echo "📊 Installing production requirements..."
    pip install -r requirements.txt
fi

# Verify installation
echo "✅ Verifying installation..."
python -c "import pandas, numpy, matplotlib, seaborn, scipy, bs4; print('✅ All core packages imported successfully!')"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To activate the environment in the future, run:"
echo "  source $ENV_NAME/bin/activate"
echo ""
echo "To deactivate the environment, run:"
echo "  deactivate"
echo ""
echo "To run the analysis notebook:"
echo "  jupyter lab enhanced_analysis.ipynb"
echo ""
echo "Happy analyzing! 📊🎮"
