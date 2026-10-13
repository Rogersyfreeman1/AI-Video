"""
Video Generator - Create videos from scripts
Uses MoviePy to create slideshow-style videos with text overlays.
"""

import os
import random
from pathlib import Path

try:
    from moviepy.editor import TextClip, ColorClip, CompositeVideoClip, concatenate_videoclips
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

from config import (
    OUTPUT_DIR, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS,
    BACKGROUND_COLORS, TEXT_COLOR, FONT_SIZE_TITLE, FONT_SIZE_BODY
)


class VideoGenerator:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(exist_ok=True)

    def create_video(self, script_data, topic, output_filename=None):
        """
        Create a video from script data.
        Returns path to created video file.
        """
        if not MOVIEPY_AVAILABLE:
            print("MoviePy not installed. Creating a placeholder video file.")
            return self._create_placeholder(script_data, topic, output_filename)

        if output_filename is None:
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_topic = safe_topic.replace(' ', '_').lower()
            output_filename = f"{safe_topic}_video.mp4"

        output_path = self.output_dir / output_filename

        # Build clips for each section
        clips = []

        # Title card (hook)
        title_clip = self._make_text_clip(
            script_data.get("title", topic),
            script_data.get("hook", "")[:100],
            duration=4,
            is_title=True
        )
        if title_clip:
            clips.append(title_clip)

        # Section clips
        for section in script_data.get("sections", []):
            clip = self._make_text_clip(
                section.get("title", ""),
                section.get("content", "")[:200],
                duration=6
            )
            if clip:
                clips.append(clip)

        # CTA clip
        cta_clip = self._make_text_clip(
            "Thanks for Watching!",
            "Like, Subscribe, and Comment Below!",
            duration=4,
            is_title=True
        )
        if cta_clip:
            clips.append(cta_clip)

        if not clips:
            print("No clips created, using placeholder")
            return self._create_placeholder(script_data, topic, output_filename)

        # Concatenate all clips
        try:
            final_video = concatenate_videoclips(clips, method="compose")
            final_video.write_videofile(
                str(output_path),
                fps=VIDEO_FPS,
                codec="libx264",
                audio=False,
                verbose=False,
                logger=None
            )
            print(f"Video created: {output_path}")
            return str(output_path)
        except Exception as e:
            print(f"Video creation failed ({e}), creating placeholder")
            return self._create_placeholder(script_data, topic, output_filename)

    def _make_text_clip(self, title, body, duration=5, is_title=False):
        """Create a single text clip with background"""
        if not MOVIEPY_AVAILABLE:
            return None

        try:
            # Pick random background color
            bg_color = random.choice(BACKGROUND_COLORS)

            # Background
            bg = ColorClip(
                size=(VIDEO_WIDTH, VIDEO_HEIGHT),
                color=bg_color,
                duration=duration
            )

            # Title text
            title_size = FONT_SIZE_TITLE if is_title else FONT_SIZE_BODY
            title_clip = TextClip(
                title,
                fontsize=title_size,
                color='white',
                size=(VIDEO_WIDTH - 100, None),
                method='caption',
                align='center'
            ).set_position(('center', 0.3), relative=True).set_duration(duration)

            # Body text (truncated)
            if body:
                body_clip = TextClip(
                    body[:300],
                    fontsize=28,
                    color='white',
                    size=(VIDEO_WIDTH - 200, None),
                    method='caption',
                    align='center'
                ).set_position(('center', 0.6), relative=True).set_duration(duration)

                video = CompositeVideoClip([bg, title_clip, body_clip])
            else:
                video = CompositeVideoClip([bg, title_clip])

            return video

        except Exception as e:
            print(f"Clip creation failed: {e}")
            return None

    def _create_placeholder(self, script_data, topic, output_filename):
        """Create a placeholder text file when video generation isn't available"""
        if output_filename is None:
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_topic = safe_topic.replace(' ', '_').lower()
            output_filename = f"{safe_topic}_video.txt"

        output_path = self.output_dir / output_filename

        with open(output_path, 'w') as f:
            f.write(f"Video Script: {topic}\n")
            f.write(f"=" * 50 + "\n\n")
            f.write(f"HOOK:\n{script_data.get('hook', '')}\n\n")
            for i, section in enumerate(script_data.get('sections', []), 1):
                f.write(f"SECTION {i}: {section.get('title', '')}\n")
                f.write(f"{section.get('content', '')}\n\n")
            f.write(f"CALL TO ACTION:\n{script_data.get('call_to_action', '')}\n")

        print(f"Placeholder created: {output_path} (install MoviePy + FFmpeg for real videos)")
        return str(output_path)
