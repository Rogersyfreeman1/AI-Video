"""
Script Generator - AI-powered video script writing
Generates engaging YouTube video scripts from topics.
Works with OpenAI API if available, falls back to templates in demo mode.
"""

import os
import random

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from config import OPENAI_API_KEY, LENGTH_CONFIG


class ScriptGenerator:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.client = None

        if self.api_key and self.api_key != "your_openai_api_key_here" and OPENAI_AVAILABLE:
            try:
                self.client = OpenAI(api_key=self.api_key)
                self.use_ai = True
            except Exception:
                self.use_ai = False
        else:
            self.use_ai = False

    def generate_script(self, topic, length="medium"):
        """
        Generate a full video script for a topic.
        Returns dict with: title, hook, sections, call_to_action, full_script
        """
        if self.use_ai:
            return self._generate_with_ai(topic, length)
        else:
            return self._generate_with_template(topic, length)

    def _generate_with_ai(self, topic, length):
        """Generate script using OpenAI GPT"""
        config = LENGTH_CONFIG.get(length, LENGTH_CONFIG["medium"])

        prompt = f"""Write a YouTube video script about: {topic}

Requirements:
- Length: {length} video (~{config['duration']} seconds)
- Structure: Hook (grab attention in first 10 seconds), {config['sections']} main sections, Call to Action
- Tone: Conversational, engaging, clear
- Audience: Regular people, not experts
- Each section: ~{config['words_per_section']} words

Format your response as:
HOOK: [hook text]
SECTION 1: [title]
[content]
SECTION 2: [title]
[content]
... (continue for all sections)
CALL TO ACTION: [CTA text]
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a YouTube script writer. Write engaging, clear scripts for regular people."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )

            script_text = response.choices[0].message.content
            return self._parse_script(script_text, topic)

        except Exception as e:
            print(f"AI generation failed ({e}), falling back to template mode")
            return self._generate_with_template(topic, length)

    def _generate_with_template(self, topic, length):
        """Generate script using built-in templates (demo mode, no API needed)"""
        config = LENGTH_CONFIG.get(length, LENGTH_CONFIG["medium"])

        # Hook templates
        hooks = [
            f"Did you know that {topic.lower()} could change your life? In this video, I'll show you exactly how.",
            f"Stop scrolling! If you want to learn about {topic.lower()}, this is the video for you.",
            f"Everyone is talking about {topic.lower()} — but most people get it wrong. Let me show you the right way.",
            f"What if I told you {topic.lower()} is easier than you think? Let me prove it.",
        ]

        # Section templates
        section_templates = [
            ("What Is {topic}?", "Let's start with the basics. {topic} is something anyone can learn, and I'll break it down simply for you."),
            ("Why It Matters", "Here's why {topic} matters for you. It can save you time, save you money, and open new opportunities."),
            ("How To Get Started", "Getting started is easier than you think. You don't need expensive equipment or special skills. Just follow these steps."),
            ("Common Mistakes", "Most people make these mistakes when starting with {topic}. Avoid them and you'll be ahead of 90% of people."),
            ("Pro Tips", "Here are some pro tips that experts use. These small tricks make a big difference."),
            ("Real Examples", "Let me share a real example of how this works in practice. This is not theory — this is real life."),
            ("Your Next Steps", "Now you know the basics. Here's exactly what to do next to get started today."),
            ("Final Thoughts", "Remember, everyone starts somewhere. The most important thing is to take that first step today."),
        ]

        hook = random.choice(hooks)
        num_sections = min(config["sections"], len(section_templates))
        sections = []

        for i in range(num_sections):
            title_template, content_template = section_templates[i]
            title = title_template.format(topic=topic)
            content = content_template.format(topic=topic)
            # Expand content to meet word count
            content = self._expand_content(content, topic, config["words_per_section"])
            sections.append({"title": title, "content": content})

        cta = f"If this video helped you, hit the like button and subscribe for more videos about {topic.lower()} and similar topics. Drop a comment below and tell me what you want to learn next. Thanks for watching!"

        full_script = f"{hook}\n\n"
        for section in sections:
            full_script += f"{section['title']}\n{section['content']}\n\n"
        full_script += f"{cta}"

        return {
            "title": topic,
            "hook": hook,
            "sections": sections,
            "call_to_action": cta,
            "full_script": full_script,
            "mode": "template"
        }

    def _expand_content(self, content, topic, target_words):
        """Expand content to reach target word count"""
        additions = [
            f" This is important because {topic.lower()} affects your daily life in ways you might not realize.",
            f" Think about it: when you understand {topic.lower()}, you make better decisions.",
            f" The key is to start small and build up. You don't need to be perfect on day one.",
            f" Many successful people started exactly where you are right now.",
            f" Remember, consistency beats perfection every time.",
        ]

        words = content.split()
        while len(words) < target_words:
            addition = random.choice(additions)
            words.extend(addition.split())

        return " ".join(words[:target_words])

    def _parse_script(self, script_text, topic):
        """Parse AI-generated script into structured format"""
        lines = script_text.strip().split("\n")
        hook = ""
        sections = []
        cta = ""
        current_section = None

        for line in lines:
            line = line.strip()
            if line.startswith("HOOK:"):
                hook = line.replace("HOOK:", "").strip()
            elif line.startswith("SECTION"):
                if current_section:
                    sections.append(current_section)
                title = line.split(":", 1)[1].strip() if ":" in line else line
                current_section = {"title": title, "content": ""}
            elif line.startswith("CALL TO ACTION:"):
                if current_section:
                    sections.append(current_section)
                    current_section = None
                cta = line.replace("CALL TO ACTION:", "").strip()
            elif current_section and line:
                current_section["content"] += " " + line

        if current_section:
            sections.append(current_section)

        if not hook:
            hook = f"Welcome! Today we're talking about {topic}."
        if not cta:
            cta = "Don't forget to like and subscribe!"

        full_script = script_text

        return {
            "title": topic,
            "hook": hook,
            "sections": sections,
            "call_to_action": cta,
            "full_script": full_script,
            "mode": "ai"
        }

    def generate_ideas(self, niche, count=5):
        """Generate video ideas from a niche"""
        if self.use_ai:
            try:
                prompt = f"Generate {count} YouTube video ideas for the niche: {niche}. Each idea should be a catchy, clickable title. Return only the titles, one per line."
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.8
                )
                ideas = [line.strip() for line in response.choices[0].message.content.strip().split("\n") if line.strip()]
                return ideas[:count]
            except Exception:
                pass

        # Template ideas
        templates = [
            f"5 Things You Didn't Know About {niche}",
            f"How to Get Started with {niche} (Beginner Guide)",
            f"The Truth About {niche} Nobody Tells You",
            f"{niche} for Beginners: Everything You Need to Know",
            f"10 Mistakes to Avoid in {niche}",
            f"How I Made Money with {niche}",
            f"{niche} Explained in 5 Minutes",
            f"Is {niche} Worth It in 2026?",
            f"Best {niche} Tips for Beginners",
            f"{niche} vs. The Alternatives: Which Is Better?",
        ]
        return random.sample(templates, min(count, len(templates)))
