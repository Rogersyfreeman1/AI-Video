#!/usr/bin/env python3
"""
AI Video System - Main CLI
Automated YouTube content creation from topics.

Usage:
    python main.py --topic "How to Save Money"
    python main.py --topic "Best Budget Phones" --length short
    python main.py --niche "personal finance" --ideas 5
    python main.py --topic "My Topic" --script-only
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.script_generator import ScriptGenerator
from src.video_generator import VideoGenerator
from src.thumbnail_generator import ThumbnailGenerator
from src.seo_optimizer import SEOOptimizer
from src.youtube_uploader import YouTubeUploader
from src.performance_tracker import PerformanceTracker


def main():
    parser = argparse.ArgumentParser(
        description="AI Video System - Create YouTube videos automatically",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --topic "How to Save Money on Groceries"
  python main.py --topic "Best Budget Phones 2026" --length short
  python main.py --topic "My Topic" --script-only
  python main.py --niche "personal finance" --ideas 5
        """
    )

    parser.add_argument("--topic", type=str, help="Video topic")
    parser.add_argument("--niche", type=str, help="Generate video ideas from a niche")
    parser.add_argument("--ideas", type=int, default=5, help="Number of ideas to generate (with --niche)")
    parser.add_argument("--length", type=str, default="medium",
                        choices=["short", "medium", "long"],
                        help="Video length: short (1 min), medium (5 min), long (10 min)")
    parser.add_argument("--script-only", action="store_true",
                        help="Generate script only, no video")
    parser.add_argument("--thumbnail-only", action="store_true",
                        help="Generate thumbnail only")
    parser.add_argument("--upload", action="store_true",
                        help="Upload to YouTube after creating (requires YouTube API setup)")
    parser.add_argument("--privacy", type=str, default="private",
                        choices=["private", "unlisted", "public"],
                        help="YouTube privacy setting for uploads")
    parser.add_argument("--summary", action="store_true",
                        help="Show performance summary of all videos")

    args = parser.parse_args()

    # Performance summary
    if args.summary:
        tracker = PerformanceTracker()
        tracker.print_summary()
        return

    # Generate ideas from niche
    if args.niche:
        print(f"\nGenerating {args.ideas} video ideas for niche: {args.niche}\n")
        gen = ScriptGenerator()
        ideas = gen.generate_ideas(args.niche, args.ideas)
        for i, idea in enumerate(ideas, 1):
            print(f"{i}. {idea}")
        print(f"\nTo create a video from an idea, run:")
        print(f'  python main.py --topic "{ideas[0]}"')
        return

    # Need a topic for video creation
    if not args.topic:
        parser.print_help()
        print("\nError: --topic is required (unless using --niche or --summary)")
        sys.exit(1)

    topic = args.topic
    print(f"\n{'='*60}")
    print(f"AI VIDEO SYSTEM")
    print(f"Topic: {topic}")
    print(f"Length: {args.length}")
    print(f"{'='*60}\n")

    # Step 1: Generate script
    print("Step 1: Generating script...")
    script_gen = ScriptGenerator()
    script_data = script_gen.generate_script(topic, args.length)
    print(f"  Mode: {script_data.get('mode', 'unknown')}")
    print(f"  Sections: {len(script_data.get('sections', []))}")
    print(f"  Script ready!\n")

    if args.script_only:
        print("SCRIPT:")
        print("-" * 60)
        print(script_data["full_script"])
        print("-" * 60)
        return

    # Step 2: Generate SEO metadata
    print("Step 2: Optimizing for YouTube SEO...")
    seo = SEOOptimizer()
    seo_data = seo.optimize(topic, script_data)
    print(f"  Title: {seo_data['title']}")
    print(f"  Tags: {', '.join(seo_data['tags'][:5])}...")
    print(f"  SEO ready!\n")

    # Step 3: Generate thumbnail
    if args.thumbnail_only:
        print("Step 3: Generating thumbnail...")
        thumb_gen = ThumbnailGenerator()
        thumb_path = thumb_gen.create_thumbnail(topic)
        print(f"  Thumbnail saved: {thumb_path}\n")
        return

    print("Step 3: Generating thumbnail...")
    thumb_gen = ThumbnailGenerator()
    thumb_path = thumb_gen.create_thumbnail(topic)
    print(f"  Thumbnail saved: {thumb_path}\n")

    # Step 4: Create video
    print("Step 4: Creating video...")
    video_gen = VideoGenerator()
    video_path = video_gen.create_video(script_data, topic)
    print(f"  Video saved: {video_path}\n")

    # Step 5: Track performance
    tracker = PerformanceTracker()
    video_id = None

    # Step 6: Upload to YouTube (if requested)
    if args.upload:
        print("Step 5: Uploading to YouTube...")
        uploader = YouTubeUploader()
        video_id = uploader.upload_video(
            video_path,
            seo_data["title"],
            seo_data["description"],
            seo_data["tags"],
            privacy=args.privacy
        )
        if video_id:
            print(f"  Uploaded! Video ID: {video_id}\n")
        else:
            print("  Upload skipped (see message above)\n")
    else:
        print("Step 5: Skipping YouTube upload (use --upload to upload)")
        print(f"  Video saved locally: {video_path}")
        print(f"  To upload later, use YouTube Studio or run with --upload\n")

    # Track it
    tracker.add_video(topic, video_path, thumb_path, seo_data["title"], video_id)

    print(f"{'='*60}")
    print("DONE!")
    print(f"{'='*60}")
    print(f"Video: {video_path}")
    print(f"Thumbnail: {thumb_path}")
    print(f"Title: {seo_data['title']}")
    if video_id:
        print(f"YouTube: https://www.youtube.com/watch?v={video_id}")
    print(f"\nNext steps:")
    print(f"  - Watch your video in the output/ folder")
    print(f"  - Upload to YouTube (if not already)")
    print(f"  - Run 'python main.py --summary' to see all your videos")


if __name__ == "__main__":
    main()
