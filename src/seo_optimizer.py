"""
SEO Optimizer - YouTube titles, descriptions, and tags
Generates SEO-optimized metadata for YouTube videos.
"""

import random


class SEOOptimizer:
    def __init__(self):
        pass

    def optimize(self, topic, script_data=None):
        """
        Generate SEO-optimized title, description, and tags for a topic.
        Returns dict with title, description, tags.
        """
        title = self._generate_title(topic)
        description = self._generate_description(topic, script_data)
        tags = self._generate_tags(topic)

        return {
            "title": title,
            "description": description,
            "tags": tags
        }

    def _generate_title(self, topic):
        """Generate clickable YouTube title"""
        # Title patterns that get clicks
        patterns = [
            f"{topic} - Everything You Need to Know",
            f"How to {topic} (Beginner Guide 2026)",
            f"5 Things You Didn't Know About {topic}",
            f"{topic} Explained in 5 Minutes",
            f"The Truth About {topic} Nobody Tells You",
            f"{topic} for Beginners - Start Here!",
            f"Why {topic} Matters (And How to Get Started)",
        ]
        return random.choice(patterns)

    def _generate_description(self, topic, script_data=None):
        """Generate YouTube description with timestamps and links"""
        description = f"In this video, we cover {topic.lower()} in detail. Whether you're a complete beginner or looking to improve, this video has everything you need.\n\n"

        if script_data and script_data.get("sections"):
            description += "TIMESTAMPS:\n"
            time = 0
            for i, section in enumerate(script_data["sections"]):
                mins = time // 60
                secs = time % 60
                description += f"{mins:02d}:{secs:02d} - {section.get('title', '')}\n"
                time += 60  # Assume ~60 sec per section

            description += "\n"

        description += f"""What you'll learn:
- The basics of {topic.lower()}
- How to get started today
- Common mistakes to avoid
- Pro tips from experts

If this video helped you, please LIKE and SUBSCRIBE for more content!

# {topic.replace(' ', '')} #tutorial #howto #beginner
"""
        return description

    def _generate_tags(self, topic):
        """Generate YouTube tags"""
        # Base tags from topic
        topic_words = topic.lower().split()
        base_tags = [topic.lower()]

        # Add variations
        for word in topic_words:
            if len(word) > 3:
                base_tags.append(word)

        # Generic high-performing tags
        generic_tags = [
            "tutorial",
            "how to",
            "beginner guide",
            "tips",
            "2026",
            "learn",
            "explained",
            "step by step",
        ]

        # Topic-specific tags
        topic_tags = [
            f"how to {topic.lower()}",
            f"{topic.lower()} tutorial",
            f"{topic.lower()} for beginners",
            f"best {topic.lower()} tips",
            f"{topic.lower()} explained",
        ]

        all_tags = base_tags + topic_tags + generic_tags

        # Deduplicate and limit to 15 tags (YouTube best practice)
        seen = set()
        unique_tags = []
        for tag in all_tags:
            if tag.lower() not in seen:
                seen.add(tag.lower())
                unique_tags.append(tag)

        return unique_tags[:15]
