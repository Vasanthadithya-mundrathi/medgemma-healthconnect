#!/bin/bash
# Quick Start Script for MedGemma HealthConnect

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║         MedGemma HealthConnect Quick Start                ║"
echo "║         Privacy-First Healthcare AI                       ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo -e "${GREEN}✅ Python found:${NC} $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo ""
    echo -e "${YELLOW}⚠️  Dependencies not installed${NC}"
    echo "Installing dependencies (this may take a few minutes)..."
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${GREEN}✅ Dependencies already installed${NC}"
fi

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env configuration..."
    cp .env.example .env
    echo -e "${GREEN}✅ Configuration file created${NC}"
fi

# Run tests
echo ""
echo "Running system tests..."
python tests/test_structure.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed${NC}"
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi

# Display information
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                   Ready to Launch!                        ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}Starting MedGemma HealthConnect...${NC}"
echo ""
echo "The application will open in your browser at:"
echo "http://localhost:8501"
echo ""
echo "To stop the application, press Ctrl+C"
echo ""
echo "⚠️  Note: First run will download AI models (~2-4GB)"
echo "   This is a one-time download and may take several minutes."
echo ""

# Start Streamlit
streamlit run app.py
