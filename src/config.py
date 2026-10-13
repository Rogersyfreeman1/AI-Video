"""
AI Video System - Configuration
Settings for video generation, thumbnails, and YouTube.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# Project paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
SRC_DIR = BASE_DIR / "src"

# Create output dir if it doesn't exist
OUTPUT_DIR.mkdir(exist_ok=True)

# API Keys (from .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
YOUTUBE_CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "client_secrets.json")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "")

# Video settings
VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1280"))
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "720"))
VIDEO_FPS = int(os.getenv("VIDEO_FPS", "24"))
VIDEO_CODEC = "libx264"

# Thumbnail settings
THUMBNAIL_WIDTH = 1280
THUMBNAIL_HEIGHT = 720

# Script settings
DEFAULT_VIDEO_LENGTH = "medium"  # short, medium, long
LENGTH_CONFIG = {
    "short": {"duration": 60, "sections": 3, "words_per_section": 80},
    "medium": {"duration": 300, "sections": 5, "words_per_section": 150},
    "long": {"duration": 600, "sections": 8, "words_per_section": 200},
}

# Colors for video backgrounds (RGB)
BACKGROUND_COLORS = [
    (30, 30, 60),      # Dark blue
    (60, 20, 20),      # Dark red
    (20, 60, 20),      # Dark green
    (40, 40, 40),      # Dark gray
    (70, 40, 90),      # Purple
]

# Text colors
TEXT_COLOR = (255, 255, 255)  # White
ACCENT_COLOR = (255, 200, 0)  # Gold for highlights

# Font settings
FONT_SIZE_TITLE = 72
FONT_SIZE_BODY = 48
FONT_SIZE_SMALL = 32
