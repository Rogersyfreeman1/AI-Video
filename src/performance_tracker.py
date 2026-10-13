"""
Performance Tracker - Track YouTube video performance
Stores video stats in a local JSON file. No API needed for basic tracking.
"""

import json
import os
from datetime import datetime
from pathlib import Path

from config import OUTPUT_DIR


class PerformanceTracker:
    def __init__(self):
        self.tracking_file = OUTPUT_DIR / "video_performance.json"
        self.data = self._load_data()

    def _load_data(self):
        """Load existing tracking data"""
        if self.tracking_file.exists():
            try:
                with open(self.tracking_file, 'r') as f:
                    return json.load(f)
            except:
                return {"videos": []}
        return {"videos": []}

    def _save_data(self):
        """Save tracking data"""
        with open(self.tracking_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_video(self, topic, video_path, thumbnail_path, title, video_id=None):
        """Add a video to tracking"""
        entry = {
            "topic": topic,
            "title": title,
            "video_path": str(video_path),
            "thumbnail_path": str(thumbnail_path),
            "youtube_video_id": video_id,
            "youtube_url": f"https://www.youtube.com/watch?v={video_id}" if video_id else None,
            "created_at": datetime.now().isoformat(),
            "views": 0,
            "likes": 0,
            "comments": 0,
            "status": "uploaded" if video_id else "local_only"
        }
        self.data["videos"].append(entry)
        self._save_data()
        print(f"Video tracked: {title}")
        return entry

    def update_stats(self, video_id, views=None, likes=None, comments=None):
        """Update stats for a video"""
        for video in self.data["videos"]:
            if video.get("youtube_video_id") == video_id:
                if views is not None:
                    video["views"] = views
                if likes is not None:
                    video["likes"] = likes
                if comments is not None:
                    video["comments"] = comments
                video["last_updated"] = datetime.now().isoformat()
                self._save_data()
                return video
        return None

    def get_summary(self):
        """Get summary of all videos"""
        videos = self.data["videos"]
        total = len(videos)
        uploaded = sum(1 for v in videos if v.get("youtube_video_id"))
        local_only = total - uploaded
        total_views = sum(v.get("views", 0) for v in videos)

        return {
            "total_videos": total,
            "uploaded": uploaded,
            "local_only": local_only,
            "total_views": total_views,
            "videos": videos
        }

    def print_summary(self):
        """Print a nice summary"""
        summary = self.get_summary()
        print("\n" + "="*50)
        print("VIDEO PERFORMANCE SUMMARY")
        print("="*50)
        print(f"Total videos: {summary['total_videos']}")
        print(f"Uploaded to YouTube: {summary['uploaded']}")
        print(f"Local only: {summary['local_only']}")
        print(f"Total views: {summary['total_views']}")
        print("="*50)

        for video in summary["videos"]:
            print(f"\n- {video['title']}")
            print(f"  Created: {video['created_at'][:10]}")
            print(f"  Status: {video['status']}")
            if video.get("youtube_url"):
                print(f"  URL: {video['youtube_url']}")
            print(f"  Views: {video.get('views', 0)} | Likes: {video.get('likes', 0)}")
