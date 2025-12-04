#!/bin/bash
# Simple script to run the Wheel of Fortune game with commentary

echo "🎪 Starting Wheel of Fortune with FREE AI Commentary..."
echo ""

cd "$(dirname "$0")/src/PlayGame"

# Check if python3 exists
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python not found!"
    echo "Please install Python 3.x"
    exit 1
fi

echo "Using: $PYTHON_CMD"
echo ""

# Run the demo first
echo "🎭 Running demo to show features..."
$PYTHON_CMD demo_commentary.py

echo ""
echo "🎮 Now starting the interactive game..."
echo "Press Ctrl+C to exit at any time"
echo ""

# Run the main game
$PYTHON_CMD play_with_commentary.py smart smart smart