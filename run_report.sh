#!/bin/bash
# Helper script to run the AI-RRM Report Generator

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=== AI-RRM Report Generator ==="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment not found${NC}"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}Please edit .env with your DNA Center credentials before running${NC}"
    echo "Run: nano .env"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Create output directory if it doesn't exist
mkdir -p output

# Run the script with provided arguments
echo -e "${GREEN}Starting AI-RRM report generation...${NC}"
python airrm_report.py "$@"

# Check exit code
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Report generated successfully!${NC}"
    echo "Check the output/ directory for your PDF report"
else
    echo -e "${RED}✗ Report generation failed${NC}"
    echo "Check airrm_report.log for details or run with --log-level DEBUG"
fi
