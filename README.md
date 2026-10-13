# AI Video System — Automated YouTube Content Creation

Build YouTube videos automatically. Type a topic, get a full video: script, visuals, thumbnail, title, description, tags — ready to upload.

Built for regular people, not just engineers. If you can type a topic, you can make a video.

## What It Does

1. **Script Generator** — Takes your topic, writes a full video script (hook, main points, call to action)
2. **Video Generator** — Turns the script into a video (slideshow with text overlays, background music optional)
3. **Thumbnail Generator** — Creates eye-catching YouTube thumbnails (1280x720)
4. **SEO Optimizer** — Writes YouTube titles, descriptions, and tags optimized for search
5. **YouTube Uploader** — Uploads directly to your YouTube channel via YouTube API
6. **Performance Tracker** — Tracks views, likes, comments for your videos

## Quick Start

### 1. Install

```bash
git clone https://github.com/Rogersyfreeman1/AI-Video.git
cd AI-Video
pip install -r requirements.txt
```

### 2. Set Up API Keys

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

You need:
- `OPENAI_API_KEY` — Get from https://platform.openai.com/api-keys
- `YOUTUBE_API_KEY` — Get from Google Cloud Console (for uploads)
- `YOUTUBE_CLIENT_SECRETS_FILE` — Path to your OAuth client secrets JSON

**No keys?** The system still works in **demo mode** — it uses built-in templates to generate scripts and videos without AI. Perfect for testing.

### 3. Make Your First Video

```bash
python main.py --topic "How to Save Money on Groceries"
```

That's it. The system will:
- Generate a script
- Create the video (saved to `output/`)
- Generate a thumbnail
- Write SEO title, description, tags
- Ask if you want to upload to YouTube

### 4. More Options

```bash
# Specify video length (short, medium, long)
python main.py --topic "Best Budget Phones 2026" --length short

# Generate script only (no video)
python main.py --topic "5 Morning Habits" --script-only

# Generate thumbnail only
python main.py --topic "How to Start a Business" --thumbnail-only

# Batch: generate 5 video ideas from one niche
python main.py --niche "personal finance" --ideas 5
```

## Project Structure

```
AI-Video/
├── main.py                  # Main CLI — start here
├── requirements.txt         # Python dependencies
├── .env.example            # Template for API keys
├── config.py               # Settings (video size, fonts, etc.)
├── src/
│   ├── script_generator.py  # AI script writing
│   ├── video_generator.py   # Video creation (MoviePy)
│   ├── thumbnail_generator.py # Thumbnail creation (Pillow)
│   ├── seo_optimizer.py     # Titles, descriptions, tags
│   ├── youtube_uploader.py  # YouTube API upload
│   └── performance_tracker.py # Track video stats
└── output/                  # Generated videos go here
```

## How It Works

### Without API Keys (Demo Mode)
Uses built-in templates and patterns to generate solid scripts and videos. No AI needed. Good for testing and learning.

### With OpenAI API Key
Uses GPT to write engaging, unique scripts tailored to your topic and audience. Much better quality, more variety.

### With YouTube API
Uploads directly to your channel. Requires OAuth setup (one-time). See `YOUTUBE_SETUP.md` for step-by-step.

## Video Style

Videos are slideshow-style: text overlays on colored backgrounds, with scene transitions. Clean, readable, works for:
- Educational / explainer videos
- List videos ("Top 5...")
- How-to tutorials
- Motivational content
- Product reviews

For more advanced video (AI-generated footage, voiceover), see the roadmap in `ROADMAP.md`.

## Requirements

- Python 3.8+
- FFmpeg (for video processing) — install from https://ffmpeg.org/
- Internet connection (for API calls, optional for demo mode)

## For Poor People, By Poor People

This project is built for regular people who want to earn from YouTube without expensive equipment or technical skills. You don't need a camera, a studio, or editing software. You need a topic and a computer.

Roger Freeman built this for his family and for millions of people below the poverty line who need a way to earn. If you can type, you can create.

## License

MIT License — free to use, modify, and share.

## Support

Issues? Questions? Open an issue on GitHub or contact Roger at rogersy@lassygeneralstore.com.
