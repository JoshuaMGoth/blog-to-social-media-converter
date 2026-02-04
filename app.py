# app.py
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import requests
import json
import re
from bs4 import BeautifulSoup
import os
import base64
import io
from dotenv import load_dotenv
import logging
from PIL import Image
import subprocess
from datetime import datetime
import shutil

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)

# Pre-load API keys from .env at module level
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPAI_API_KEY = os.getenv('DEEPAI_API_KEY')

app = Flask(__name__)
CORS(app)
app.logger.setLevel("DEBUG")

# Log loaded keys (masked) at startup
app.logger.info(f"DEEPSEEK_API_KEY loaded: {'yes' if DEEPSEEK_API_KEY else 'NO'}")
app.logger.info(f"DEEPAI_API_KEY loaded: {'yes' if DEEPAI_API_KEY else 'NO'}")

class BlogToInstagram:
    def __init__(self, deepseek_api_key, deepai_api_key=None):
        self.deepseek_api_key = deepseek_api_key
        self.deepai_api_key = deepai_api_key
        self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"
        self.deepai_url = "https://api.deepai.org/api/text2img"
        self.headers_deepseek = {
            "Authorization": f"Bearer {deepseek_api_key}",
            "Content-Type": "application/json"
        }
        # DeepAI expects the API key in the 'Api-Key' HTTP header
        self.headers_deepai = {
            "Api-Key": deepai_api_key if deepai_api_key else ""
        }

    def extract_blog_content(self, url):
        """Extract text content from a blog URL"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove scripts and styles
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()

            # Get main content
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            return text[:5000]  # Limit to 5000 chars
        except Exception as e:
            return f"Error fetching blog: {str(e)}"

    def generate_instagram_post(self, blog_content):
        """Generate Instagram post content from blog"""
        prompt = f"""
        Create an engaging Instagram post from this blog content.

        Requirements:
        1. Create a catchy caption (max 2200 characters)
        2. Suggest 5-10 relevant hashtags
        3. Format it for Instagram (use emojis, line breaks)
        4. Keep it conversational and engaging
        5. Suggest a visual concept for the post

        Blog content: {blog_content[:3000]}

        Format your response as JSON:
        {{
            "caption": "the Instagram caption here",
            "hashtags": ["#hashtag1", "#hashtag2"],
            "image_description": "detailed description of an image that would complement this post"
        }}
        """

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a social media expert who creates engaging Instagram posts from blog content."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000
        }

        try:
            response = requests.post(self.deepseek_url, json=payload, headers=self.headers_deepseek)
            result = response.json()

            if 'choices' in result:
                content = result['choices'][0]['message']['content']
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    return {
                        "caption": content,
                        "hashtags": ["#blog", "#content", "#instagram"],
                        "image_description": "A visually appealing image related to the blog topic"
                    }
            else:
                return {"error": "No response from AI"}

        except Exception as e:
            return {"error": str(e)}

    def generate_facebook_post(self, blog_content):
        """Generate Facebook post content from blog - scroll-stopping format"""
        prompt = f"""
        Create a scroll-stopping Facebook post from this blog content. The goal is to make people STOP scrolling and CLICK the link to read the full blog.

        Use this 5-PART STRUCTURE:

        🎯 PART 1 - THE HOOK (1-2 sentences)
        A provocative, relatable statement or question that creates instant curiosity. Make them feel seen.

        💬 PART 2 - THE BODY (3-5 short paragraphs)
        Expand on the hook with emotional, relatable content. Use short paragraphs. Create tension between the easy path and the right path. Make them nod along.

        🔗 PART 3 - LINK & CTA (1-2 sentences)
        Tease what they'll learn/feel by reading the full blog. End with "Read it here: [Link to blog]"

        💭 PART 4 - ENGAGEMENT PROMPT (1 question)
        Ask a specific question that invites them to share their experience. Include your own brief answer as an example.

        🎨 PART 5 - VISUALS GUIDE (3 options)
        Describe 3 visual options: 1) A relatable photo scene, 2) A text graphic with a key quote, 3) A short video concept

        Blog content: {blog_content[:3000]}

        Format your response as JSON:
        {{
            "hook": "The attention-grabbing opening",
            "body": "The main emotional content with short paragraphs",
            "cta": "The call-to-action with link placeholder",
            "engagement_prompt": "The question to drive comments",
            "visuals_guide": "The 3 visual options described",
            "full_post": "The complete formatted post ready to copy (Parts 1-4 combined with emojis)",
            "image_description": "The best visual concept for AI image generation"
        }}
        """

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a Facebook marketing expert who creates viral, scroll-stopping posts that drive clicks to blog links. You understand emotional hooks and engagement psychology."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1500
        }

        try:
            response = requests.post(self.deepseek_url, json=payload, headers=self.headers_deepseek)
            result = response.json()

            if 'choices' in result:
                content = result['choices'][0]['message']['content']
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    return {
                        "full_post": content,
                        "hook": "",
                        "body": "",
                        "cta": "",
                        "engagement_prompt": "",
                        "visuals_guide": "",
                        "image_description": "An engaging, relatable image for the blog topic"
                    }
            else:
                return {"error": "No response from AI"}

        except Exception as e:
            return {"error": str(e)}

    def generate_pinterest_post(self, blog_content, blog_url=""):
        """Generate Pinterest pin strategies from blog content"""
        prompt = f"""
        Analyze this blog content and create a Pinterest pin strategy for maximum engagement.

        Create 4-6 pin ideas using different pin types:
        - title: Main headline pin with the key message
        - list: Numbered key takeaways or tips
        - howto: Step-by-step guide format
        - quote: Inspiring or thought-provoking quote from content
        - statistic: Key data point or finding

        For each pin, provide:
        - type: The pin type (title, list, howto, quote, statistic)
        - focus: What this pin emphasizes
        - keyPoints: 3-4 bullet points for the pin content
        - callToAction: The CTA text
        - pinTitle: The headline text for the pin (max 60 chars)
        - pinDescription: Pinterest-optimized description (max 500 chars, keyword-rich)

        Also provide:
        - summary: Brief blog summary
        - keyTopics: 3-5 main topics
        - targetAudience: Who this content is for
        - pinterestKeywords: 8-10 SEO keywords for Pinterest search
        - boardSuggestions: 3 Pinterest board names this would fit

        Blog content: {blog_content[:3000]}

        Format your response as JSON:
        {{
            "summary": "Brief summary of the blog",
            "keyTopics": ["topic1", "topic2", "topic3"],
            "targetAudience": "Description of target audience",
            "pinterestKeywords": ["keyword1", "keyword2"],
            "boardSuggestions": ["Board Name 1", "Board Name 2", "Board Name 3"],
            "pinStrategies": [
                {{
                    "type": "title",
                    "focus": "Main message focus",
                    "keyPoints": ["point1", "point2", "point3"],
                    "callToAction": "Read More →",
                    "pinTitle": "Catchy Pin Title",
                    "pinDescription": "Pinterest-optimized description with keywords"
                }}
            ],
            "image_description": "Visual style recommendation for pin graphics"
        }}
        """

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a Pinterest marketing expert who creates viral pin strategies that drive traffic to blogs. You understand Pinterest SEO, visual design principles, and what makes pins get saved and clicked."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000
        }

        try:
            response = requests.post(self.deepseek_url, json=payload, headers=self.headers_deepseek)
            result = response.json()

            if 'choices' in result:
                content = result['choices'][0]['message']['content']
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    parsed['blog_url'] = blog_url
                    return parsed
                else:
                    return {
                        "summary": content[:200],
                        "keyTopics": ["blog", "content"],
                        "targetAudience": "Blog readers",
                        "pinterestKeywords": ["blog", "tips", "ideas"],
                        "boardSuggestions": ["Blog Posts", "Tips & Ideas", "Inspiration"],
                        "pinStrategies": [
                            {
                                "type": "title",
                                "focus": "Main blog topic",
                                "keyPoints": ["Key point from blog"],
                                "callToAction": "Read More →",
                                "pinTitle": "Blog Highlights",
                                "pinDescription": "Check out this blog post for great insights!"
                            }
                        ],
                        "image_description": "A visually appealing Pinterest-style graphic"
                    }
            else:
                return {"error": "No response from AI"}

        except Exception as e:
            return {"error": str(e)}

    def generate_post(self, blog_content, platform="instagram", blog_url=""):
        """Generate post for specified platform"""
        if platform == "facebook":
            return self.generate_facebook_post(blog_content)
        elif platform == "pinterest":
            return self.generate_pinterest_post(blog_content, blog_url)
        else:
            return self.generate_instagram_post(blog_content)

    def generate_image_prompt(self, blog_content, image_description=""):
        """Generate a detailed image generation prompt"""
        if image_description:
            base_description = image_description
        else:
            base_description = "Create an engaging, colorful image related to the blog topic"

        prompt = f"""
        Based on this blog content and image description, create a detailed prompt for AI image generation.

        Blog excerpt: {blog_content[:1000]}

        Original image description: {base_description}

        Create a detailed prompt that includes:
        1. Main subject and composition
        2. Style (photorealistic, illustration, digital art, etc.)
        3. Color scheme
        4. Lighting and mood
        5. Additional artistic details

        Make the prompt specific and suitable for AI image generation.
        """

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You create detailed, specific prompts for AI image generators."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500
        }

        try:
            response = requests.post(self.deepseek_url, json=payload, headers=self.headers_deepseek)
            result = response.json()
            detailed = result['choices'][0]['message']['content']
        except Exception:
            detailed = f"Create an image showing: {base_description}"

        # Use AI to generate a short, one-sentence prompt from the detailed one
        short = self.summarize_prompt_with_ai(detailed)
        return {"detailed": detailed, "short": short}

    def summarize_prompt_with_ai(self, detailed_prompt: str) -> str:
        """Use DeepSeek AI to create a concise one-line image description.
        
        Examples of good output:
        - "Warm cozy living room at sunset"
        - "Mountain landscape with golden light"
        - "Modern minimalist office space"
        """
        prompt = f"""Summarize the following image description into ONE short phrase (5-8 words max) that describes the scene simply.

Do NOT include any instructions or meta-text. Just output the short descriptive phrase.

Examples of good output:
- "Cozy living room with warm sunset light"
- "Mountain landscape at golden hour"
- "Modern minimalist workspace"

Image description to summarize:
{detailed_prompt[:1500]}

Short phrase:"""

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You summarize image descriptions into short, simple phrases for AI image generation. Output ONLY the short phrase, nothing else."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 50
        }

        try:
            response = requests.post(self.deepseek_url, json=payload, headers=self.headers_deepseek)
            result = response.json()
            short = result['choices'][0]['message']['content'].strip()
            # Clean up any quotes or extra formatting
            short = short.strip('"\'')
            # Ensure it's not too long
            if len(short.split()) > 12:
                short = ' '.join(short.split()[:8])
            return short if short else "Scenic colorful image"
        except Exception as e:
            app.logger.exception("Failed to summarize prompt with AI")
            return self.summarize_prompt_fallback(detailed_prompt)

    def summarize_prompt_fallback(self, text: str) -> str:
        """Fallback: Create a concise one-line summary using simple text processing."""
        try:
            # Remove parenthetical content
            t = re.sub(r"\([^)]*\)", "", text)
            # Split by sentences/clauses
            clause = re.split(r"[\.\n\;\-\—]", t)[0]

            # Tokenize into words and remove punctuation
            words = re.findall(r"\w+", clause)
            stopwords = set(["the","a","an","and","or","with","in","on","for","of","to","by","is","are","that","this","as","from","create","image","showing","here","detailed","prompt","ai","generation"])
            content = [w for w in words if w.lower() not in stopwords]

            if not content:
                content = re.findall(r"\w+", text)[:6]

            short_words = content[:6]
            short = ' '.join([w.capitalize() for w in short_words])

            if len(short.split()) < 2:
                short = 'Scenic Image'

            return short
        except Exception:
            return 'Scenic Image'

    def generate_image_with_deepai(self, prompt):
        """Generate an image using DeepAI API"""
        if not self.deepai_api_key:
            return {"error": "DeepAI API key is not configured"}
        # Some DeepAI clients expect the key in different header casings.
        header_variants = [
            {"Api-Key": self.deepai_api_key},
            {"api-key": self.deepai_api_key},
            {"Api-key": self.deepai_api_key}
        ]

        last_result = None
        for hdr in header_variants:
            try:
                response = requests.post(
                    self.deepai_url,
                    data={'text': prompt[:1000]},
                    headers=hdr,
                    timeout=30
                )

                # Try to decode JSON; if that fails, capture text
                try:
                    result = response.json()
                except Exception:
                    result = {"raw_text": response.text}

                app.logger.debug(f"DeepAI response with headers {hdr.keys()}: {result}")
                last_result = result

                # Check for common success keys
                output_url = None
                if isinstance(result, dict):
                    if 'output_url' in result:
                        output_url = result['output_url']
                    elif 'output' in result and isinstance(result['output'], list) and result['output']:
                        output_url = result['output'][0]
                    elif 'output_urls' in result and isinstance(result['output_urls'], list) and result['output_urls']:
                        output_url = result['output_urls'][0]

                if output_url:
                    try:
                        img_response = requests.get(output_url, timeout=30)
                        img_response.raise_for_status()
                        img_base64 = base64.b64encode(img_response.content).decode('utf-8')
                        return {
                            "success": True,
                            "image_url": output_url,
                            "image_base64": img_base64,
                            "image_format": "png"
                        }
                    except Exception as e:
                        app.logger.exception("Failed to download DeepAI output_url")
                        return {"error": f"Failed to download generated image: {str(e)}"}

                # If we reach here, no usable image in this response; try next header

            except Exception as e:
                app.logger.exception("DeepAI request failed for header variant")
                last_result = {"exception": str(e)}

        # No header variant produced an image
        app.logger.debug(f"DeepAI final result after trying headers: {last_result}")
        # Provide the last result details to help the frontend/user debug
        # If DeepAI rejected the prompt as unsafe, try sanitizing and retry once
        try:
            err_text = ''
            if isinstance(last_result, dict):
                err_text = str(last_result.get('err') or last_result.get('error') or last_result.get('status') or '')
            else:
                err_text = str(last_result)

            if 'unsafe' in err_text.lower() or 'potentially unsafe' in err_text.lower():
                app.logger.info('DeepAI rejected prompt as unsafe — attempting auto-sanitization and retry')
                sanitized = self.sanitize_prompt(prompt)
                app.logger.debug(f"Sanitized prompt: {sanitized}")

                # Retry once with sanitized prompt
                for hdr in header_variants:
                    try:
                        response = requests.post(
                            self.deepai_url,
                            data={'text': sanitized[:1000]},
                            headers=hdr,
                            timeout=30
                        )
                        try:
                            result = response.json()
                        except Exception:
                            result = {"raw_text": response.text}

                        app.logger.debug(f"DeepAI retry response with headers {hdr.keys()}: {result}")

                        # Try to extract image as before
                        output_url = None
                        if isinstance(result, dict):
                            if 'output_url' in result:
                                output_url = result['output_url']
                            elif 'output' in result and isinstance(result['output'], list) and result['output']:
                                output_url = result['output'][0]
                            elif 'output_urls' in result and isinstance(result['output_urls'], list) and result['output_urls']:
                                output_url = result['output_urls'][0]

                        if output_url:
                            img_response = requests.get(output_url, timeout=30)
                            img_response.raise_for_status()
                            img_base64 = base64.b64encode(img_response.content).decode('utf-8')
                            return {
                                "success": True,
                                "image_url": output_url,
                                "image_base64": img_base64,
                                "image_format": "png"
                            }
                    except Exception:
                        app.logger.exception('DeepAI retry request failed')

        except Exception:
            app.logger.exception('Error while checking for unsafe prompt')

        return {"error": f"DeepAI API error: {last_result}"}

    def sanitize_prompt(self, prompt: str) -> str:
        """Sanitize prompts by removing risky words and adding a safe prefix.

        This is a conservative, best-effort sanitization to avoid DeepAI content filters.
        """
        blacklist = [
            'blood', 'gore', 'violent', 'kill', 'killing', 'murder', 'dead', 'injured',
            'weapon', 'gun', 'knife', 'bomb', 'porn', 'sexual', 'nude', 'naked',
            'celebrity', 'famous', 'real person', 'face of', 'graphic'
        ]

        sanitized = prompt
        for word in blacklist:
            sanitized = re.sub(r'(?i)\b' + re.escape(word) + r"\b", '', sanitized)

        # Collapse multiple spaces and trim
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()

        # Prepend a safety prefix to steer generation away from risky content
        prefix = 'A safe, family-friendly, non-violent photorealistic image of'
        # If the prompt already sounds like a short phrase, append it; otherwise combine
        if len(sanitized) == 0:
            return prefix + ' a scenic, colorful scene.'
        return f"{prefix} {sanitized}"


# ========== SETTINGS HELPER FUNCTIONS ==========

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'app_settings.json')

def get_default_settings():
    """Return default settings structure with all API providers"""
    return {
        "text_ai": {
            "deepseek": "",
            "openai": "",
            "anthropic": "",
            "google_gemini": "",
            "cohere": "",
            "mistral": "",
            "groq": "",
            "xai": "",
            "perplexity": ""
        },
        "image_ai": {
            "deepai": "",
            "openai_image": "",
            "stability_ai": "",
            "replicate": "",
            "leonardo": "",
            "midjourney": "",
            "ideogram": "",
            "flux": ""
        }
    }

def load_settings():
    """Load settings from JSON file"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                saved = json.load(f)
                # Merge with defaults to ensure all keys exist
                defaults = get_default_settings()
                for category in defaults:
                    if category not in saved:
                        saved[category] = defaults[category]
                    else:
                        for key in defaults[category]:
                            if key not in saved[category]:
                                saved[category][key] = defaults[category][key]
                return saved
    except Exception as e:
        app.logger.error(f"Error loading settings: {e}")
    return get_default_settings()

def save_settings(settings):
    """Save settings to JSON file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception as e:
        app.logger.error(f"Error saving settings: {e}")
        return False


# ========== FLASK ROUTES ==========

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Settings page for API keys"""
    saved = False
    if request.method == 'POST':
        current_settings = load_settings()
        
        # Text AI providers
        current_settings['text_ai']['deepseek'] = request.form.get('deepseek_api_key', '')
        current_settings['text_ai']['openai'] = request.form.get('openai_api_key', '')
        current_settings['text_ai']['anthropic'] = request.form.get('anthropic_api_key', '')
        current_settings['text_ai']['google_gemini'] = request.form.get('google_gemini_api_key', '')
        current_settings['text_ai']['cohere'] = request.form.get('cohere_api_key', '')
        current_settings['text_ai']['mistral'] = request.form.get('mistral_api_key', '')
        current_settings['text_ai']['groq'] = request.form.get('groq_api_key', '')
        current_settings['text_ai']['xai'] = request.form.get('xai_api_key', '')
        current_settings['text_ai']['perplexity'] = request.form.get('perplexity_api_key', '')
        
        # Image AI providers
        current_settings['image_ai']['deepai'] = request.form.get('deepai_api_key', '')
        current_settings['image_ai']['openai_image'] = request.form.get('openai_image_api_key', '')
        current_settings['image_ai']['stability_ai'] = request.form.get('stability_api_key', '')
        current_settings['image_ai']['replicate'] = request.form.get('replicate_api_key', '')
        current_settings['image_ai']['leonardo'] = request.form.get('leonardo_api_key', '')
        current_settings['image_ai']['midjourney'] = request.form.get('midjourney_api_key', '')
        current_settings['image_ai']['ideogram'] = request.form.get('ideogram_api_key', '')
        current_settings['image_ai']['flux'] = request.form.get('flux_api_key', '')
        
        save_settings(current_settings)
        saved = True
    
    settings_data = load_settings()
    return render_template('settings.html', settings=settings_data, saved=saved)

@app.route('/api/settings', methods=['GET'])
def get_settings_api():
    """API endpoint to get settings (keys masked)"""
    settings_data = load_settings()
    # Mask all API keys for security
    masked = {
        "text_ai": {k: ("****" + v[-4:] if v and len(v) > 4 else "") for k, v in settings_data.get('text_ai', {}).items()},
        "image_ai": {k: ("****" + v[-4:] if v and len(v) > 4 else "") for k, v in settings_data.get('image_ai', {}).items()}
    }
    return jsonify(masked)

@app.route('/api/process', methods=['POST'])
def process_blog():
    data = request.json
    url = data.get('url')
    platform = data.get('platform', 'instagram')  # 'instagram', 'facebook', or 'pinterest'
    # Use module-level keys loaded from .env, allow override from request
    deepseek_key = data.get('deepseek_key') or DEEPSEEK_API_KEY
    deepai_key = data.get('deepai_key') or DEEPAI_API_KEY
    generate_image = data.get('generate_image', False)

    app.logger.debug(f"process_blog: platform={platform}, deepseek_key present: {bool(deepseek_key)}, deepai_key present: {bool(deepai_key)}")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    if not deepseek_key:
        return jsonify({"error": "DeepSeek API key is required. Please set DEEPSEEK_API_KEY in .env"}), 400

    processor = BlogToInstagram(deepseek_key, deepai_key)

    # Extract blog content
    blog_content = processor.extract_blog_content(url)

    if "Error" in blog_content:
        return jsonify({"error": blog_content}), 500

    # Generate post based on platform (pass url for Pinterest)
    post_content = processor.generate_post(blog_content, platform, url)

    # Generate detailed image prompt (returns dict with 'detailed' and 'short')
    image_prompt_result = processor.generate_image_prompt(
        blog_content,
        post_content.get('image_description', '')
    )

    # Normalize results
    if isinstance(image_prompt_result, dict):
        image_prompt_detailed = image_prompt_result.get('detailed')
        image_prompt_short = image_prompt_result.get('short')
    else:
        image_prompt_detailed = image_prompt_result
        image_prompt_short = None

    response_data = {
        "blog_summary": blog_content[:500] + "...",
        "platform": platform,
        "post_content": post_content,  # Generic key for any platform
        "instagram_post": post_content if platform == "instagram" else None,  # Keep for backwards compat
        "facebook_post": post_content if platform == "facebook" else None,
        "pinterest_post": post_content if platform == "pinterest" else None,
        "image_prompt": image_prompt_detailed,
        "image_prompt_short": image_prompt_short,
        "success": True
    }

    # Generate image if requested and API key is available
    if generate_image and deepai_key:
        image_result = processor.generate_image_with_deepai(image_prompt_detailed)
        response_data["image_generation"] = image_result

    return jsonify(response_data)

@app.route('/api/generate_image', methods=['POST'])
def generate_image_endpoint():
    data = request.json
    prompt = data.get('prompt')
    # Use module-level key loaded from .env, allow override from request
    deepai_key = data.get('deepai_key') or DEEPAI_API_KEY

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    if not deepai_key:
        return jsonify({"error": "DeepAI API key is required. Please set DEEPAI_API_KEY in .env"}), 400

    processor = BlogToInstagram("dummy_key", deepai_key)
    result = processor.generate_image_with_deepai(prompt)

    return jsonify(result)


@app.route('/api/mock_image', methods=['GET'])
def mock_image_endpoint():
    """Return a tiny sample base64 PNG for frontend testing without DeepAI."""
    # 1x1 transparent PNG
    sample_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII="
    return jsonify({
        "success": True,
        "image_base64": sample_base64,
        "image_format": "png"
    })


if __name__ == '__main__':
    # Configure file logging so we can tail logs
    handler = logging.FileHandler('flask.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Also capture werkzeug (access) logs
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.DEBUG)
    werkzeug_logger.addHandler(handler)

    app.run(debug=True, port=5000)
