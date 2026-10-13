"""
Thumbnail Generator - Create eye-catching YouTube thumbnails
Uses Pillow to generate 1280x720 thumbnails with bold text.
"""

import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from config import OUTPUT_DIR, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT


class ThumbnailGenerator:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(exist_ok=True)

    def create_thumbnail(self, topic, output_filename=None):
        """
        Create a YouTube thumbnail for a topic.
        Returns path to thumbnail image.
        """
        if output_filename is None:
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_topic = safe_topic.replace(' ', '_').lower()
            output_filename = f"{safe_topic}_thumbnail.png"

        output_path = self.output_dir / output_filename

        # Background - vibrant gradient-like colors
        bg_colors = [
            (255, 50, 50),    # Red
            (50, 100, 255),   # Blue
            (255, 150, 0),    # Orange
            (150, 0, 255),    # Purple
            (0, 200, 100),    # Green
        ]
        bg_color = random.choice(bg_colors)

        # Create image
        img = Image.new('RGB', (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), bg_color)
        draw = ImageDraw.Draw(img)

        # Add some visual elements (circles, rectangles for style)
        for _ in range(5):
            x = random.randint(0, THUMBNAIL_WIDTH)
            y = random.randint(0, THUMBNAIL_HEIGHT)
            r = random.randint(50, 200)
            # Semi-transparent overlay effect (darker shade)
            darker = tuple(max(0, c - 30) for c in bg_color)
            draw.ellipse([x-r, y-r, x+r, y+r], fill=darker)

        # Try to load a bold font, fall back to default
        try:
            # Try common font paths
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "C:\\Windows\\Fonts\\arialbd.ttf",
            ]
            font = None
            for fp in font_paths:
                try:
                    font = ImageFont.truetype(fp, 90)
                    break
                except:
                    continue
            if font is None:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        # Main text - split topic into lines
        words = topic.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + " " + word) > 20:
                lines.append(current_line.strip())
                current_line = word
            else:
                current_line += " " + word
        if current_line:
            lines.append(current_line.strip())

        # Draw text (centered, with shadow for readability)
        y = THUMBNAIL_HEIGHT // 2 - (len(lines) * 60) // 2
        for line in lines:
            # Get text width for centering
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (THUMBNAIL_WIDTH - text_width) // 2

            # Shadow
            draw.text((x + 4, y + 4), line, fill=(0, 0, 0), font=font)
            # Main text (white with yellow accent)
            draw.text((x, y), line, fill=(255, 255, 255), font=font)
            y += 110

        # Add "PLAY" indicator or arrow (simple triangle)
        # Bottom right corner - play button circle
        cx, cy = THUMBNAIL_WIDTH - 120, THUMBNAIL_HEIGHT - 120
        draw.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], fill=(255, 255, 255))
        draw.polygon([(cx - 15, cy - 25), (cx - 15, cy + 25), (cx + 25, cy)], fill=(255, 0, 0))

        # Save
        img.save(output_path, "PNG")
        print(f"Thumbnail created: {output_path}")
        return str(output_path)

    def create_thumbnail_with_text(self, title, subtitle="", output_filename=None):
        """Create thumbnail with custom title and subtitle"""
        return self.create_thumbnail(title, output_filename)
