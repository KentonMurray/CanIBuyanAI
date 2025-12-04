"""
Configuration for Wheel of Fortune Solve Advisor
Handles API key management for Google Gemini
"""

import os
from pathlib import Path

# Try to load from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, will use environment variables directly

# Gemini API Configuration
# Set your API key here or in a .env file as GEMINI_API_KEY="your-key"
# Get a free key at: https://makersuite.google.com/app/apikey
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Model settings
GEMINI_MODEL = "gemini-2.0-flash"  # Fast and cost-effective

# Confidence thresholds for recommendations
CONFIDENCE_HIGH = 75  # Above this = "Solve now!"
CONFIDENCE_MEDIUM = 50  # Above this = "Consider solving"
CONFIDENCE_LOW = 25  # Below this = "Keep guessing letters"


def get_api_key():
    """Get the Gemini API key from environment or prompt user."""
    if GEMINI_API_KEY:
        return GEMINI_API_KEY
    
    # Check for .env file
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"\'')
    
    return None


def set_api_key(api_key: str):
    """Save API key to .env file for future use."""
    env_path = Path(__file__).parent / ".env"
    
    # Read existing content
    existing_lines = []
    if env_path.exists():
        with open(env_path, "r") as f:
            existing_lines = [line for line in f if not line.startswith("GEMINI_API_KEY=")]
    
    # Write back with new key
    with open(env_path, "w") as f:
        f.writelines(existing_lines)
        f.write(f'GEMINI_API_KEY="{api_key}"\n')
    
    print(f"API key saved to {env_path}")
